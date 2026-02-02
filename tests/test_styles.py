#!/usr/bin/env python3
"""
Test suite for Afghan cover art styles and generators.

Run with:
    pytest -v tests/test_styles.py
"""

import os
import sys
import pytest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from afcover.styles import (
    get_style_names,
    get_regional_names,
    get_occasion_names,
    build_style_prompt,
    STYLES,
    REGIONAL_STYLES,
    OCCASIONS,
)
from afcover.generator import generate_cover
from shared.api import estimate_cost


class TestStyles:
    """Test suite for Afghan cover art style definitions and generators."""

    def test_style_names_available(self):
        """Check that styles are available and properly defined."""
        styles = get_style_names()
        assert len(styles) >= 6, "Expected at least 6 styles"
        assert "traditional" in styles, "Traditional style is missing"
        assert "modern" in styles, "Modern style is missing"
        assert "fusion" in styles, "Fusion style is missing"

    def test_regional_names_available(self):
        """Check that regional modifiers are available."""
        regions = get_regional_names()
        assert len(regions) >= 5, "Expected at least 5 regional styles"
        assert "kabuli" in regions, "Kabuli regional style is missing"
        assert "herati" in regions, "Herati regional style is missing"

    def test_occasion_names_available(self):
        """Check that occasion themes are available."""
        occasions = get_occasion_names()
        assert len(occasions) >= 3, "Expected at least 3 occasion themes"
        assert "nowruz" in occasions, "Nowruz occasion is missing"
        assert "eid" in occasions, "Eid occasion is missing"

    def test_style_required_attributes(self):
        """Check that each style has the required attributes."""
        for name, style in STYLES.items():
            assert "name" in style, f"Style {name} is missing 'name'"
            assert "description" in style, f"Style {name} is missing 'description'"
            assert "elements" in style, f"Style {name} is missing 'elements'"
            assert "colors" in style, f"Style {name} is missing 'colors'"
            assert "typography" in style, f"Style {name} is missing 'typography'"
            assert "mood" in style, f"Style {name} is missing 'mood'"

    def test_regional_required_attributes(self):
        """Check that each regional style has the required attributes."""
        for name, regional in REGIONAL_STYLES.items():
            assert "name" in regional, f"Regional style {name} is missing 'name'"
            assert "modifier" in regional, f"Regional style {name} is missing 'modifier'"
            assert "visual_elements" in regional, f"Regional style {name} is missing 'visual_elements'"
            assert len(regional["visual_elements"]) >= 2, f"Regional style {name} needs at least 2 visual elements"

    def test_style_prompt_generation(self):
        """Test that style prompts are generated correctly."""
        for style_name in get_style_names():
            prompt = build_style_prompt(style_name)
            assert len(prompt) > 100, f"Style {style_name} prompt too short"
            assert style_name in prompt.lower(), f"Style {style_name} name not in prompt"
            assert STYLES[style_name]["name"] in prompt, f"Style {style_name} full name not in prompt"
            assert "color" in prompt.lower(), f"Style {style_name} missing color info"
            
    def test_style_regional_combinations(self):
        """Test all style and regional combinations."""
        for style_name in get_style_names():
            for regional_name in get_regional_names():
                prompt = build_style_prompt(style_name, regional=regional_name)
                assert len(prompt) > 150, f"{style_name}+{regional_name} prompt too short"
                assert style_name in prompt.lower(), f"Style {style_name} name not in prompt"
                assert regional_name in prompt.lower(), f"Regional {regional_name} name not in prompt"
                assert REGIONAL_STYLES[regional_name]["modifier"] in prompt, f"Regional {regional_name} modifier missing"

    def test_style_occasion_combinations(self):
        """Test style and occasion combinations."""
        for style_name in ["traditional", "modern"]:  # Test subset for speed
            for occasion_name in get_occasion_names():
                prompt = build_style_prompt(style_name, occasion=occasion_name)
                assert len(prompt) > 150, f"{style_name}+{occasion_name} prompt too short"
                assert occasion_name in prompt.lower(), f"Occasion {occasion_name} name not in prompt"
                assert OCCASIONS[occasion_name]["name"] in prompt, f"Occasion {occasion_name} full name missing"

    def test_custom_elements(self):
        """Test adding custom elements to style prompt."""
        custom_elements = ["specific test element one", "another custom element"]
        prompt = build_style_prompt("traditional", custom_elements=custom_elements)
        
        for element in custom_elements:
            assert element in prompt, f"Custom element '{element}' not found in prompt"

    def test_dry_run_generation(self):
        """Test dry run generation with cost estimate."""
        # Skip if no sample image available - this is a dummy path for example
        sample_image = Path(__file__).parent / "fixtures" / "sample.jpg"
        if not sample_image.exists():
            pytest.skip(f"Sample image not found: {sample_image}")
        
        result = generate_cover(
            reference_images=[str(sample_image)],
            title="Test Album",
            artist="Test Artist",
            style="traditional",
            dry_run=True,
        )
        
        assert result["dry_run"] is True
        assert "estimated_cost" in result
        assert "prompt_preview" in result
        assert result["style"] == "traditional"
        assert "message" in result and "Would generate" in result["message"]

    def test_cost_estimation(self):
        """Test cost estimation function."""
        # 1K/2K cost
        assert estimate_cost(1, "1K") == 0.15
        assert estimate_cost(4, "2K") == 0.60
        
        # 4K cost (2x)
        assert estimate_cost(1, "4K") == 0.30
        assert estimate_cost(4, "4K") == 1.20

    def test_style_cultural_elements(self):
        """Ensure styles have appropriate Afghan cultural elements."""
        for name, style in STYLES.items():
            has_afghan_element = False
            # Check in name, description and elements
            texts_to_check = [style["name"], style["description"]] + style["elements"]
            
            for text in texts_to_check:
                if any(term in text.lower() for term in ["afghan", "افغان", "dari", "pashto", "nastaliq", "kabul"]):
                    has_afghan_element = True
                    break
            
            assert has_afghan_element, f"Style {name} lacks explicit Afghan cultural elements"

    def test_invalid_style_raises_error(self):
        """Test that invalid style names raise appropriate error."""
        with pytest.raises(ValueError, match="Unknown style"):
            build_style_prompt("non_existent_style")

    @pytest.mark.parametrize("style_name", ["traditional", "modern", "fusion"])
    def test_typography_inclusion(self, style_name):
        """Test typography inclusion/exclusion in prompts."""
        # With typography
        prompt_with_typo = build_style_prompt(style_name, include_typography=True)
        assert "typography" in prompt_with_typo.lower(), f"Style {style_name} missing typography with flag enabled"
        
        # Without typography
        prompt_without_typo = build_style_prompt(style_name, include_typography=False)
        assert STYLES[style_name]["typography"] not in prompt_without_typo, \
            f"Style {style_name} has typography despite flag disabled"


# Only run if executed directly (not imported)
if __name__ == "__main__":
    # Create pytest.ini file if it doesn't exist
    pytest_ini = Path(__file__).parent.parent / "pytest.ini"
    if not pytest_ini.exists():
        with open(pytest_ini, "w") as f:
            f.write("[pytest]\n")
            f.write("testpaths = tests\n")
            f.write("python_files = test_*.py\n")
    
    # Run the tests
    pytest.main(["-v", __file__])
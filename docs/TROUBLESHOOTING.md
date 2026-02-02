# NanoBot Troubleshooting Guide

This guide addresses common issues and solutions for the NanoBot tools, with a focus on the `afcover` Afghan music cover art generator.

## Table of Contents
- [API Issues](#api-issues)
- [Image Generation Issues](#image-generation-issues)
- [Style Issues](#style-issues)
- [Regional Modifier Issues](#regional-modifier-issues)
- [Text/Typography Issues](#texttypography-issues)
- [Cost and Optimization](#cost-and-optimization)
- [Reference Library Issues](#reference-library-issues)
- [Installation Issues](#installation-issues)
- [Common Error Messages](#common-error-messages)

## API Issues

### API Key Not Found
```
ValueError: FAL_KEY not found. Please create a .env file with your API key.
```

**Solution**:
1. Get a fal.ai API key at https://fal.ai/dashboard/keys
2. Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```
3. Edit the `.env` file and add your API key:
   ```
   FAL_KEY=your_actual_api_key
   ```

### API Rate Limiting
```
API Error 429: Too many requests
```

**Solution**:
1. Reduce the frequency of requests
2. Implement exponential backoff between retries
3. Contact fal.ai to discuss rate limit increases for your account

### API Connection Timeout
```
Connection Error: Connection timed out
```

**Solution**:
1. Check your internet connection
2. Verify that fal.ai services are operational
3. Try again later or from a different network

### API Unexpected Response
```
RuntimeError: API Error 400: Invalid request
```

**Solution**:
1. Check for malformed parameters
2. Ensure reference images are valid formats (JPG, PNG)
3. Try simplifying your request
4. Check fal.ai status for service issues

## Image Generation Issues

### No Images Generated
```
Error: No images returned
```

**Solution**:
1. Check that reference images are accessible and valid
2. Simplify your prompt and try again
3. Verify that your API key has sufficient credits

### Blurry or Low-Quality Results

**Solution**:
1. Use higher quality reference images
2. Try increasing resolution to 2K or 4K
3. Add "high resolution, sharp details, professional quality" to custom prompt
4. Add "blurry, pixelated, low quality" to negative prompt

### Generic or Non-Afghan Results

**Solution**:
1. Use explicit Afghan cultural references in custom prompt:
   ```
   --custom "authentic Afghan carpet patterns, Nastaliq calligraphy style, lapis lazuli blue accents"
   ```
2. Use more culturally specific reference images
3. Add a regional modifier:
   ```
   --regional kabuli
   ```
4. Try a different style that's more culturally specific:
   ```
   --style traditional
   ```

### Strange or Unwanted Elements

**Solution**:
1. Use a negative prompt to exclude specific elements:
   ```
   --negative-prompt "faces, text, watermarks, logos, Western symbols"
   ```
2. Be more specific about what you want:
   ```
   --custom "minimal composition with Afghan geometric patterns only"
   ```
3. Try different reference images
4. Use a seed from a previous generation that was closer to desired output:
   ```
   --seed 12345
   ```

## Style Issues

### Style Not Recognizable

**Issue**: Generated image doesn't match the selected style.

**Solution**:
1. Use style-specific reference images (from the style reference library)
2. Add style description to custom prompt:
   ```
   --style traditional --custom "ornate gold patterns, jewel tones, classic Afghan aesthetic"
   ```
3. Check if your reference images conflict with the style
4. Try increasing the weight of style elements:
   ```
   --custom "STRONG traditional Afghan style influence, elaborate ornate patterns"
   ```

### Conflicting Style Elements

**Issue**: Image contains mixed elements from different styles.

**Solution**:
1. Use fewer reference images
2. Choose reference images that match your desired style
3. Be more explicit about excluding unwanted elements:
   ```
   --negative-prompt "modern elements, Western style, minimalism"
   ```

### Missing Key Style Elements

**Solution**:
1. Explicitly request key elements in custom prompt:
   ```
   --style ghazal --custom "include calligraphy, parchment texture, ink wash aesthetic"
   ```
2. Use reference images that clearly showcase these elements

## Regional Modifier Issues

### Regional Style Not Applied

**Issue**: Regional modifier doesn't seem to influence the result.

**Solution**:
1. Add regional specifics to custom prompt:
   ```
   --regional herati --custom "incorporate Herati tile patterns and Persian artistic traditions"
   ```
2. Use reference images from that region
3. Try a different style that may work better with regional modifiers:
   ```
   --style traditional --regional herati
   ```

### Overemphasized Regional Elements

**Issue**: Regional elements dominate and clash with the base style.

**Solution**:
1. Use a more compatible base style
2. Add balancing instructions to custom prompt:
   ```
   --custom "subtle regional influence, balanced with main style"
   ```
3. Try a different combination of style and regional modifier

## Text/Typography Issues

### No Clear Space for Text

**Issue**: Image design doesn't leave appropriate space for title/artist text.

**Solution**:
1. Explicitly specify text placement:
   ```
   --text-placement title_prominent
   ```
2. Add clear instructions for text space:
   ```
   --custom "leave upper third clear for Dari title text, clean background for typography"
   ```
3. Try a style with better typography accommodation:
   ```
   --style modern --text-placement title_bottom
   ```

### Wrong Typography Style Space

**Issue**: Image design suggests Western typography rather than Dari/Pashto.

**Solution**:
1. Explicitly request Dari/Pashto typography space:
   ```
   --custom "design for Nastaliq or Naskh Persian/Dari typography, right-to-left text flow"
   ```
2. Choose a more traditional style:
   ```
   --style traditional --text-placement integrated_calligraphy
   ```

## Cost and Optimization

### Unexpected High Costs

**Issue**: Generation costs more than expected.

**Solution**:
1. Always use dry run first to estimate costs:
   ```
   --dry-run
   ```
2. Reduce number of variations:
   ```
   --num 1
   ```
3. Use lower resolution for drafts:
   ```
   --resolution 1K
   ```
4. Ensure `limit_generations=True` is set to prevent prompt injection

### Cost-Efficient Testing Workflow

For optimal cost efficiency:

1. **Plan**: Start with a dry run to check prompt and estimate cost
   ```
   --dry-run
   ```

2. **Explore**: Generate 1-2 low-res variations to test style
   ```
   --resolution 1K --num 2
   ```

3. **Refine**: Adjust prompt based on results
   ```
   --custom "refined based on previous test"
   ```

4. **Finalize**: Generate one high-quality final version
   ```
   --resolution 2K --num 1 --seed 12345
   ```

### Resolution Selection Guide

- **1K ($0.15)**: Use for draft concepts, style exploration
- **2K ($0.15)**: Good for final versions, streaming platforms
- **4K ($0.30)**: Only for print materials, large displays

## Reference Library Issues

### References Not Found

```
Warning: No references found for artist: Artist Name
```

**Solution**:
1. Check that the artist/style name is correct (case-sensitive)
2. Add references to the library first:
   ```python
   from afcover.library import add_artist_reference
   add_artist_reference("Artist Name", "path/to/image.jpg")
   ```
3. Verify reference library structure:
   ```bash
   python -m afcover.cli --list-references
   ```

### Adding References Fails

**Solution**:
1. Ensure the image file exists and is a supported format
2. Check file permissions
3. Verify library directory structure exists:
   ```bash
   mkdir -p afcover/references/artists/Artist
   mkdir -p afcover/references/styles/style_name
   ```
4. Try adding with explicit metadata:
   ```python
   add_artist_reference(
       "Artist Name",
       "path/to/image.jpg",
       metadata={"source": "known_album_cover"}
   )
   ```

## Installation Issues

### Missing Dependencies

```
ModuleNotFoundError: No module named 'module_name'
```

**Solution**:
1. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. For specific missing dependencies:
   ```bash
   pip install missing_package_name
   ```
3. Check Python version compatibility (Python 3.6+ required)

### Permission Issues

```
PermissionError: [Errno 13] Permission denied
```

**Solution**:
1. Check file/directory permissions:
   ```bash
   chmod -R u+rw .
   ```
2. Ensure you have write permissions in the output directory
3. Try running with elevated permissions (if appropriate)

## Common Error Messages

### "RuntimeError: API Error 400: Invalid request format"

**Cause**: Malformed API request

**Solution**:
1. Check reference image formats (JPG, PNG supported)
2. Ensure all required parameters are present
3. Verify prompt isn't too long (try shortening it)

### "ValueError: Unknown style: style_name"

**Cause**: Using an invalid style name

**Solution**:
1. Check available styles:
   ```bash
   python -m afcover.cli --list-styles
   ```
2. Use only supported styles from the list

### "RuntimeError: API Error 401: Unauthorized"

**Cause**: Invalid or expired API key

**Solution**:
1. Check your `.env` file contains the correct API key
2. Get a new key from fal.ai dashboard
3. Ensure the key has not expired or been revoked

### "FileNotFoundError: Reference file not found"

**Cause**: Reference image path is incorrect

**Solution**:
1. Check file path and name (case-sensitive)
2. Use absolute paths if relative paths are not working
3. Verify the file exists and is readable

### "RuntimeError: API Error 429: Rate limit exceeded"

**Cause**: Too many requests in a short time period

**Solution**:
1. Add delay between requests
2. Implement exponential backoff
3. Contact fal.ai for increased limits

## Advanced Troubleshooting

### Debug Mode

To enable more detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Inspect API Requests

To see the exact payload being sent:

```python
from afcover.generator import AfghanCoverGenerator

generator = AfghanCoverGenerator()
result = generator.generate(
    reference_images=["ref.jpg"],
    title="Debug Test",
    style="traditional",
    dry_run=True,
)
print(f"Full prompt: {result['prompt_preview']}")
```

### Validate Style Prompts

```python
from afcover.styles import build_style_prompt

# Test a style + regional combination
prompt = build_style_prompt("traditional", regional="kabuli")
print(prompt)

# Check if prompt contains expected elements
assert "traditional" in prompt.lower()
assert "kabuli" in prompt.lower()
```

### Reset Environment

If you're experiencing persistent issues, try resetting:

```bash
# Remove any cached files
rm -rf __pycache__
rm -rf afcover/__pycache__

# Reset environment
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Test with minimal parameters
python -m afcover.cli --list-styles
```

## Still Need Help?

If you've tried these solutions and still experience issues:

1. Check the project GitHub repository for updates or known issues
2. Submit a detailed bug report including:
   - Full error message
   - Command/code that produced the error
   - Expected vs. actual results
   - Python and dependency versions
3. Contact the package maintainer
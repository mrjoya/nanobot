# NanoBot Cost Optimization Guide

This guide provides strategies for optimizing costs when using NanoBot tools, particularly the `afcover` Afghan music cover art generator.

## Understanding Pricing

### Base Costs

| Resolution | Cost per Image | Best Use Case |
|------------|----------------|---------------|
| 1K | $0.15 | Draft concepts, testing |
| 2K | $0.15 | Standard releases, social media |
| 4K | $0.30 | Print, high-resolution displays |

### Cost Calculation

Total cost = Cost per image × Number of variations

For example:
- 3 variations at 1K resolution = 3 × $0.15 = $0.45
- 1 variation at 4K resolution = 1 × $0.30 = $0.30

## Cost Optimization Strategies

### 1. Always Start with Dry Runs

Use dry runs to preview costs and prompts without generating images:

```bash
# CLI dry run
python -m afcover.cli \
  --ref reference.jpg \
  --style traditional \
  --title "Album Title" \
  --dry-run

# Python API dry run
from afcover.generator import generate_cover
result = generate_cover(
    reference_images=["reference.jpg"],
    title="Album Title",
    style="traditional",
    dry_run=True,
)
print(f"Estimated cost: {result['estimated_cost']}")
print(f"Prompt: {result['prompt_preview']}")
```

### 2. Strategic Resolution Selection

- **Start with 1K** for concept exploration
- **Use 2K** for final versions (same price as 1K, better quality)
- **Reserve 4K** only for print materials

### 3. Efficient Variation Strategy

Rather than generating many variations at once:

1. Generate 1-2 variations at 1K first
2. Review and refine the prompt
3. Generate 1 final version at 2K with refined prompt

This approach gives better results while using fewer total variations.

### 4. Leverage Seed Values

When you find a generation you like, note the random seed and reuse it:

```bash
# Generate with a specific seed
python -m afcover.cli \
  --ref reference.jpg \
  --style traditional \
  --seed 12345
```

This allows you to:
1. Test a concept at 1K resolution
2. Regenerate the exact same concept at 2K/4K 
3. Make minor prompt adjustments while maintaining the core concept

### 5. Optimize Reference Images

- **Size**: Compress reference images before upload (1-2MB is sufficient)
- **Quality**: Use clear, relevant reference images for better first-try results
- **Combination**: Use 1-2 carefully chosen references instead of many random ones

### 6. Use the Reference Library

The reference library provides consistent, optimized images without needing to upload the same references repeatedly:

```bash
# Add to library once
from afcover.library import add_artist_reference
add_artist_reference("Artist Name", "path/to/best_reference.jpg")

# Use many times
python -m afcover.cli --artist-ref "Artist Name" --title "New Album"
```

### 7. Prompt Engineering for Fewer Iterations

Write specific, detailed prompts to get better results on the first try:

**Inefficient (may require multiple attempts):**
```
--custom "make it traditional"
```

**Efficient (more likely to succeed first time):**
```
--custom "ornate gold borders, Afghan carpet patterns in burgundy and emerald, elegant Nastaliq calligraphy space in upper third, rich jewel tones"
```

### 8. Batch Processing for Multiple Covers

When creating multiple covers for a series or album:

1. Test style concept with one representative cover at 1K
2. Once satisfied with the style, apply to all covers at 2K
3. Use the same seed across the series for consistency

```python
# Define common parameters
common_params = {
    "reference_images": ["artist_photo.jpg", "style_reference.jpg"],
    "artist": "Artist Name",
    "style": "traditional",
    "seed": 12345,  # Keep the same seed for consistency
    "resolution": "2K",
}

# Generate multiple covers efficiently
for track in ["Track 1", "Track 2", "Track 3"]:
    result = generate_cover(
        **common_params,
        title=track,
    )
```

## Cost Control Safety Features

### Limit Generations Flag

The `limit_generations=True` parameter (default) prevents prompt injection techniques that could generate more images than requested:

```python
generate_cover(
    reference_images=["ref.jpg"],
    title="Album",
    style="traditional",
    limit_generations=True,  # Default, but explicitly set for safety
)
```

### Maximum Variations Limit

The API enforces a maximum of 4 variations per request to prevent accidental high-cost operations:

```python
# This will be capped at 4 variations
generate_cover(
    reference_images=["ref.jpg"],
    title="Album",
    style="traditional",
    num_variations=10,  # Will be limited to 4
)
```

## Recommended Workflows by Budget

### Minimal Budget ($0.30-0.45 per cover)

```python
# Step 1: Dry run to check prompt (free)
result = generate_cover(
    reference_images=["ref.jpg"],
    title="Album",
    style="traditional",
    dry_run=True,
)

# Step 2: Generate 1-2 variations at 1K ($0.15-0.30)
result = generate_cover(
    reference_images=["ref.jpg"],
    title="Album",
    style="traditional",
    resolution="1K",
    num_variations=1,  # Start with 1
)

# Step 3: Final version at 2K with refinements ($0.15)
result = generate_cover(
    reference_images=["ref.jpg"],
    title="Album",
    style="traditional",
    custom_prompt="refined based on previous result",
    resolution="2K",
    num_variations=1,
)
```

### Standard Budget ($0.60-0.75 per cover)

```python
# Step 1: Explore style options at 1K ($0.45)
result = generate_cover(
    reference_images=["ref.jpg"],
    title="Album",
    style="traditional",
    resolution="1K",
    num_variations=3,
)

# Step 2: Final version at 2K with refinements ($0.15-0.30)
result = generate_cover(
    reference_images=["ref.jpg"],
    title="Album",
    style="traditional",
    custom_prompt="refined based on previous result",
    resolution="2K",
    num_variations=1,  # Or 2 for slight variations
)
```

### Professional Budget ($1.20-1.50 per cover)

```python
# Step 1: Explore style options at 1K ($0.60)
result = generate_cover(
    reference_images=["ref1.jpg", "ref2.jpg"],
    title="Album",
    style="traditional",
    resolution="1K",
    num_variations=4,
)

# Step 2: Refined variations at 2K ($0.30-0.45)
result = generate_cover(
    reference_images=["ref1.jpg", "ref2.jpg"],
    title="Album",
    style="traditional",
    custom_prompt="refined based on previous results",
    resolution="2K",
    num_variations=2,  # Or 3 for more options
)

# Step 3: Final high-res version at 4K ($0.30)
result = generate_cover(
    reference_images=["ref1.jpg", "ref2.jpg"],
    title="Album",
    style="traditional",
    custom_prompt="final refined version",
    resolution="4K",
    num_variations=1,
    seed=12345,  # Using seed from best 2K version
)
```

## Cost Comparison with Traditional Methods

| Method | Approximate Cost | Turnaround Time |
|--------|-----------------|-----------------|
| NanoBot (Basic) | $0.30-0.45 | Minutes |
| NanoBot (Professional) | $1.20-1.50 | 1 hour |
| Stock Image + Editing | $20-50 | 1-2 days |
| Freelance Designer | $50-200 | 3-7 days |
| Professional Studio | $200-500+ | 1-2 weeks |

## Bulk Pricing Strategy

When creating multiple covers for an album or series:

1. **Style Development**: Invest in exploring styles for the first cover ($0.60-0.90)
2. **Template Application**: Apply the successful style to remaining covers at minimal variation ($0.30 each)
3. **Consistency**: Use the same seed, references, and parameters across all covers

Example for a 10-track album:
- First cover exploration: $0.90
- 9 remaining covers at template price: $2.70
- Total for 10 covers: $3.60 ($0.36 per cover)

## Monthly Budget Planning

Estimate your monthly costs based on usage patterns:

| Usage Level | Covers per Month | Estimated Budget |
|-------------|-----------------|------------------|
| Occasional | 5-10 | $3-6 |
| Regular | 20-30 | $9-15 |
| Studio | 50-100 | $20-40 |
| Agency | 100+ | $40-100+ |

## Optimization Checklist

Before generating:
- [ ] Start with dry run to check cost
- [ ] Use appropriate resolution for the stage (1K for drafts, 2K/4K for finals)
- [ ] Optimize reference images (quality, relevance, size)
- [ ] Write detailed prompts to succeed on first try
- [ ] Set `limit_generations=True` for safety

After generating:
- [ ] Note seeds of successful generations for reuse
- [ ] Add successful references to library for future use
- [ ] Document successful prompt patterns
- [ ] Track costs to refine your workflow

## Conclusion

By following these optimization strategies, you can achieve professional results while keeping costs to a minimum. The key is to start simple, iterate deliberately, and use higher-cost options only when necessary for final products.
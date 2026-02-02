# Cost Control Guidelines

## ⚠️ IMPORTANT: API Usage Costs Real Money

The NanoBot project uses fal.ai's Nano Banana Pro API which has associated costs:
- Standard (1K/2K): $0.15 per image
- High-res (4K): $0.30 per image
- Each variation counts as a separate image

## Cost Control Mechanisms

To prevent unexpected charges, we've implemented several safeguards:

### 1. Dry Run Mode

All commands support a `--dry-run` flag that shows cost estimates without making API calls:

```bash
# Show cost without generating
python afcover/cli.py --dry-run --ref reference.jpg --title "Test" --artist "Test"
```

### 2. Cost Monitor

Use the cost monitoring script to track and review API usage:

```bash
# Show recent usage and cost breakdown
python scripts/cost_monitor.py report

# Set daily spending limits
python scripts/cost_monitor.py limit --daily=5.00

# Initialize cost tracking
python scripts/cost_monitor.py init
```

### 3. Environment Variables

Set these variables to control behavior:

```bash
# Skip confirmation prompts (use with caution!)
export NANOBOT_SKIP_CONFIRM=1

# Force dry-run mode for all commands
export NANOBOT_DRY_RUN=1

# Set daily spending limit
export NANOBOT_DAILY_LIMIT=10.00
```

## Development Guidelines

1. **Always use `--dry-run` during development**
2. **Limit variations to 1 when testing**
3. **Use 1K resolution for initial tests**
4. **Implement explicit confirmation for all API calls**
5. **Track all costs in the log**

## Bot Integration Safeguards

The OpenClaw bot integration includes additional safeguards:
- All commands require explicit confirmation before generating
- Cost estimates are displayed before confirmation
- Daily/session limits are enforced
- Usage history is tracked and reportable

## Cost Optimization Tips

1. **Use reference images** - They produce better results with fewer iterations
2. **Start with 1K resolution** - Only use 4K for final outputs
3. **Generate one image first** - Then create variations if needed
4. **Use effective prompts** - Better prompts = fewer iterations
5. **Leverage style presets** - They're optimized for good results

## Cost Management Best Practices

1. **Monitor regularly** - Check usage with the cost monitor
2. **Set reasonable limits** - Control daily/monthly spending
3. **Share reference libraries** - Reduce the need for experimentation
4. **Document successful approaches** - Avoid repeating expensive tests
5. **Use mock testing** - Test logic without API calls

Remember: Cost control is everyone's responsibility!
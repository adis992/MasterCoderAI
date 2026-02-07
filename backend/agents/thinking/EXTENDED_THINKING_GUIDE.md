# Building with Extended Thinking

---

Extended thinking gives Claude enhanced reasoning capabilities for complex tasks, while providing varying levels of transparency into its step-by-step thought process before it delivers its final answer.

## Supported models

Extended thinking is supported in the following models:

- Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)
- Claude Sonnet 4 (`claude-sonnet-4-20250514`)
- Claude Sonnet 3.7 (`claude-3-7-sonnet-20250219`) ([deprecated](/docs/en/about-claude/model-deprecations))
- Claude Haiku 4.5 (`claude-haiku-4-5-20251001`)
- Claude Opus 4.5 (`claude-opus-4-5-20251101`)
- Claude Opus 4.1 (`claude-opus-4-1-20250805`)
- Claude Opus 4 (`claude-opus-4-20250514`)

**Note:** API behavior differs across Claude Sonnet 3.7 and Claude 4 models, but the API shapes remain exactly the same.

## How extended thinking works

When extended thinking is turned on, Claude creates `thinking` content blocks where it outputs its internal reasoning. Claude incorporates insights from this reasoning before crafting a final response.

The API response will include `thinking` content blocks, followed by `text` content blocks.

Here's an example of the default response format:

```json
{
  "content": [
    {
      "type": "thinking",
      "thinking": "Let me analyze this step by step...",
      "signature": "WaUjzkypQ2mUEVM36O2TxuC06KN8xyfbJwyem2dw3URve/op91XWHOEBLLqIOMfFG/UvLEczmEsUjavL...."
    },
    {
      "type": "text",
      "text": "Based on my analysis..."
    }
  ]
}
```

## How to use extended thinking

Here is an example of using extended thinking in the Messages API:

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    },
    messages=[{
        "role": "user",
        "content": "Are there an infinite number of prime numbers such that n mod 4 == 3?"
    }]
)

# The response will contain summarized thinking blocks and text blocks
for block in response.content:
    if block.type == "thinking":
        print(f"\nThinking summary: {block.thinking}")
    elif block.type == "text":
        print(f"\nResponse: {block.text}")
```

To turn on extended thinking, add a `thinking` object, with the `type` parameter set to `enabled` and the `budget_tokens` to a specified token budget for extended thinking.

The `budget_tokens` parameter determines the maximum number of tokens Claude is allowed to use for its internal reasoning process. In Claude 4 models, this limit applies to full thinking tokens, and not to [the summarized output](#summarized-thinking). Larger budgets can improve response quality by enabling more thorough analysis for complex problems, although Claude may not use the entire budget allocated, especially at ranges above 32k.

`budget_tokens` must be set to a value less than `max_tokens`. However, when using [interleaved thinking with tools](#interleaved-thinking), you can exceed this limit as the token limit becomes your entire context window (200k tokens).

## Best practices and considerations for extended thinking

### Working with thinking budgets

- **Budget optimization:** The minimum budget is 1,024 tokens. We suggest starting at the minimum and increasing the thinking budget incrementally to find the optimal range for your use case. Higher token counts enable more comprehensive reasoning but with diminishing returns depending on the task.
- **Starting points:** Start with larger thinking budgets (16k+ tokens) for complex tasks and adjust based on your needs.
- **Large budgets:** For thinking budgets above 32k, we recommend using batch processing to avoid networking issues.
- **Token usage tracking:** Monitor thinking token usage to optimize costs and performance.

### Performance considerations

- **Response times:** Be prepared for potentially longer response times due to the additional processing required for the reasoning process.
- **Streaming requirements:** Streaming is required when `max_tokens` is greater than 21,333.

### Feature compatibility

- Thinking isn't compatible with `temperature` or `top_k` modifications as well as forced tool use.
- When thinking is enabled, you can set `top_p` to values between 1 and 0.95.
- You cannot pre-fill responses when thinking is enabled.
- Changes to the thinking budget invalidate cached prompt prefixes that include messages.

### Usage guidelines

- **Task selection:** Use extended thinking for particularly complex tasks that benefit from step-by-step reasoning like math, coding, and analysis.
- **Context handling:** You do not need to remove previous thinking blocks yourself. The Claude API automatically ignores thinking blocks from previous turns.
- **Prompt engineering:** Review extended thinking prompting tips to maximize Claude's thinking capabilities.

## Implementation in MasterCoderAI

The MasterCoderAI system implements extended thinking through:

1. **Agent Dispatcher Integration:** Automatic thinking activation for complex queries
2. **Model Configuration:** Per-model thinking settings and budget allocation  
3. **User Controls:** Frontend toggles for thinking parameters
4. **Performance Monitoring:** Thinking token usage tracking and optimization
5. **Context Management:** Intelligent thinking block preservation and cleanup

## Configuration Options

- **Enable Extended Thinking:** Toggle thinking on/off globally
- **Budget Tokens:** Set thinking token budget (1024 - 32000+)
- **Auto-Activation:** Automatically enable thinking for complex tasks
- **Thinking Display:** Show/hide thinking process in UI
- **Performance Mode:** Optimize for speed vs. thoroughness
- **Context Preservation:** Maintain thinking blocks across tool use

Extended thinking represents the future of AI reasoning - providing transparency into the model's thought process while delivering more accurate and well-reasoned responses.
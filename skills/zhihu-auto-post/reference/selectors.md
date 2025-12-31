# Zhihu Element Selectors Reference


Quick reference for key Zhihu UI elements (as of December 2025).


## Question Creation Flow


| Element | Primary Selector | Fallback |

|---------|-----------------|----------|

| Create button (+) | `button[aria-label='创作']` | `#Popover3-toggle` |

| Ask question menu item | `div.css-hv22zf:has-text('提问题')` | lookup text "提问题" |

| Title textarea | `textarea.Input` | click at (720, 283) |

| Description placeholder | `div#placeholder-cnm03` | lookup text "输入问题背景" |

| Description editor | `div[contenteditable='true']` | - |

| Submit button | `button:has-text('发布问题')` | lookup text "发布问题" |


## Other Actions


| Element | Selector |

|---------|----------|

| Write answer | `div.css-hv22zf:has-text('写回答')` |

| Write article | `div.css-hv22zf:has-text('写文章')` |

| Share thought | `div.css-hv22zf:has-text('发想法')` |


## Notes


- CSS class names (e.g., `css-hv22zf`) may change with Zhihu updates

- Always prefer aria-label or text-based selectors for stability

- Use `browser:browser_lookup` to find current selectors when defaults fail
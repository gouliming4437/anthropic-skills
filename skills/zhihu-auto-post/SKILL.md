---

name: zhihu-auto-post

description: Automate posting questions on Zhihu (知乎) using browser automation. Use when user asks to post a question on Zhihu, create a Zhihu question, or automate Zhihu interactions. Requires Blueprint browser MCP (@railsblueprint/blueprint-mcp) to be configured. Handles the full workflow of navigating to Zhihu, opening the question dialog, filling in title and description, and submitting.

---


# Zhihu Auto Post Skill


Post questions to Zhihu (知乎) automatically using browser automation.


## Prerequisites


- Blueprint browser MCP must be configured in Claude Desktop:

```json

"browser": {

"command": "npx",

"args": ["@railsblueprint/blueprint-mcp@latest"]

}

```

- User must be logged into Zhihu in Chrome

- Blueprint browser extension must have "Allow access to all URLs" enabled


## Workflow


### Step 1: Enable Browser and Open Zhihu


```

browser:enable client_id="zhihu-post"

browser:browser_tabs action="new" url="https://www.zhihu.com"

browser:browser_interact actions=[{"type": "wait", "timeout": 3000}]

```


### Step 2: Open Question Dialog


Hover on "+" button to reveal menu, then click "提问题":


```

browser:browser_interact actions=[{"type": "hover", "selector": "button[aria-label='创作']"}]

browser:browser_interact actions=[{"type": "wait", "timeout": 500}]

browser:browser_interact actions=[{"type": "click", "selector": "div.css-hv22zf:has-text('提问题')"}]

browser:browser_interact actions=[{"type": "wait", "timeout": 1500}]

```


### Step 3: Fill Title


The title input appears in a modal. Click at coordinates (~720, 283) then type:


```

browser:browser_interact actions=[{"type": "mouse_click", "x": 720, "y": 283}]

browser:browser_interact actions=[{"type": "type", "selector": "textarea.Input", "text": "<title>"}]

```


### Step 4: Fill Description


After typing title, click description area and type content:


```

browser:browser_interact actions=[{"type": "click", "selector": "div#placeholder-cnm03"}]

browser:browser_interact actions=[{"type": "type", "selector": "div[contenteditable='true']", "text": "<description>"}]

```


### Step 5: Submit


```

browser:browser_lookup text="发布问题"

browser:browser_interact actions=[{"type": "click", "selector": "button:has-text('发布问题')"}]

browser:browser_interact actions=[{"type": "wait", "timeout": 2000}]

browser:browser_take_screenshot

```


Success: URL changes to `https://www.zhihu.com/question/<id>`.


## Troubleshooting


- **Element not found**: Use `browser:browser_snapshot` or `browser:browser_lookup` to find elements

- **Dialog not opening**: Add wait time between hover and click

- **Selectors changed**: Use `browser:browser_lookup text="提问题"` to find by text content

- **Modal not in DOM**: Use `browser:browser_take_screenshot` to verify visual state
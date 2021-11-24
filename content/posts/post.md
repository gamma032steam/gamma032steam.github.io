---
title: "Material UI Drawer in a Div"
date: 2021-07-18T16:28:15+10:00
draft: false
---

[Try it in CodeSandbox!](https://codesandbox.io/s/material-ui-drawer-in-div-fpzt4) ✏️️

# The problem

Material UI's [drawer component](https://material-ui.com/components/drawers/) is an animated sidebar. You can use it as a navigation bar or side sheet. 

By default, the drawer is `position: fixed`, meaning it's removed from the document flow and positioned relative to the viewport. This causes two issues:
- The drawer is always stuck to the side of the screen
- The drawer doesn't respect the position of the content around it.

# Solving with absolute position

You can find an absolute position solution with React [here](https://codesandbox.io/s/material-ui-drawer-in-div-fpzt4?file=/demo.js).

There are a few important aspects:

1. Make the underlying [Material UI paper](https://material-ui.com/components/paper/) `position: absolute`. You can assign a class to it with the `classes` prop on the drawer.
2. Absolutely positioned elements place themselves relative to the nearest positioned ancestor, so make the enclosing drawer `position: relative`.
3. If you want the drawer to take space and 'push' the content, set its width conditional to whether it's open.
4. Place both the content and drawer into a flexbox, allowing the width of both elements to dynamically adjust.

# With an iframe


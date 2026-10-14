# jig

I like programming! And I like language design. Here's to jig: a semi-general purpose programming language that's above all:

- easy and fast to write
- without sacrificing readability
- and easy to pick up!

> disclaimer: everyone below does not work as of right now since i just started making jig

```jig
say "jig starts in..."
for (1..3).rev |n| { say "{n}..." }
say "jig!"
```

## Philosophy

Here's the set of guidelines that I use to shape jig:

- whatever is most common should be shortest and easiest to write
- all syntax should be easy to understand
- few special symbols each doing one thing only
- as few ways as possible to do one thing.
- fail fast

## Try it!

```shell
uv tool install git+https://github.com/TheSecondComing123/jig
<or>
uvx --from git+https://github.com/TheSecondComing123/jig jig

jig # repl
jig file.jig [args]
jig -e "a line of code"
```

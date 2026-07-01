
Have to pick image resolution; trading off quality vs speed vs memory usage

Problem with repeated generation
  │ -         extra_body={"top_p": 0.9, "temperature": 0.3},                                      │
  │ +         extra_body={"top_p": 0.9, "temperature": 0.3, "repetition_penalty": 1.3},


Lots of repetition
```python
extra_body={"top_p": 0.9, "temperature": 0.3, "repetition_penalty": 1.3},
```


Somewhat working
```python
extra_body={"top_p": 0.8, "temperature": 0.6},
```

Had to move to
```python
extra_body={"top_p": 0.9, "temperature": 0.9, "repetition_penalty": 1.3},
```
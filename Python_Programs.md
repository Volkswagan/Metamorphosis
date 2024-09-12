```python
words = "aabbbcccc"
count = {}

for word in words:
    count[word] = count.get(word, 0) + 1

output = ""
for k,v in count.items():
	output = output + f"{k}{v}"
print(output)
```
```python
text = "my name is ram, ram name is good"
words = text.replace(",", "").split()  # Remove commas and split into words
count = {}

for word in words:
    count[word] = count.get(word, 0) + 1

output = ""
for k,v in count.items():
	output = output + f"{k}{v}" + "\n"
print(output)
```

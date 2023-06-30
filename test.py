def foo():
  yield "1"
  yield "2"
  yield "3"
  return "4"

for value in foo():
  print(value)

x = foo()
print(x)
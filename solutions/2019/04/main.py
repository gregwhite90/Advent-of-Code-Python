start = 145852
end = 616942


valid = 0
for num in range(start, end + 1):
  digits = list(str(num))
  decreased = False
  for i in range(1, len(digits)):
    if digits[i] < digits [i - 1]:
      decreased = True
      break
  if decreased: continue
  repeated_digit = False
  j = 0
  while j < (len(digits) - 1):
    index = j
    while (j < len(digits) and digits[index] == digits[j]):
      j += 1
    if j - index == 2:
      repeated_digit = True
      break
  if repeated_digit and not decreased:
    valid += 1
print(valid)
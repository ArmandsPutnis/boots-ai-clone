from functions.write_to_file import write_file

test1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print(test1)

test2 = write_file("calculator", "pkg/morelorm.txt", "lorem ipsum dolor sit amet")
print(test2)

test3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print(test3)

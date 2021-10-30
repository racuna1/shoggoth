# Makefile
SRC_DIR=./src
CODE_DIR=$(SRC_DIR)/code
OUT=example
TEST_DIR=test
CODE_NAME=StudentAssignment

test:
	make -C $(TEST_DIR)

test_clean:
	make -C $(TEST_DIR) clean

StudentAssignment.o:
	gcc -c -I$(CODE_DIR) $(CODE_DIR)/*.c -o $(CODE_DIR)/$(CODE_NAME).o

main: StudentAssignment.o
	gcc -I$(CODE_DIR) $(CODE_DIR)/$(CODE_NAME).o $(SRC_DIR)/main.cpp -o $(OUT)

all: test main

clean: test_clean
	rm $(SRC_DIR)/*.o $(CODE_DIR)/*.o $(OUT)

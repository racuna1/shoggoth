/**
* C program to save a schedule of classes
*
* Completion time: 4h
*
* @author Charles Jeffries, Acuna
* @version 1.0
*/

////////////////////////////////////////////////////////////////////////////////
//INCLUDES
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

////////////////////////////////////////////////////////////////////////////////
//MACROS: CONSTANTS



////////////////////////////////////////////////////////////////////////////////
//DATA STRUCTURES
typedef enum{
    CSE = 0, EEE, EGR, SER
} Subject;

typedef struct CourseNode{
    Subject subject;
    int number;
    char teacher[1024];
    int credit_hours;
    struct CourseNode* next;
} CourseNode;


////////////////////////////////////////////////////////////////////////////////
//GLOBAL VARIABLES

//place to store course information
CourseNode* course_collection = NULL;

char* subjectStrings[] = {
        "CSE",
        "EEE",
        "EGR",
        "SER"
};

////////////////////////////////////////////////////////////////////////////////
//FORWARD DECLARATIONS
void branching(char option);
int getCreditCount();
void course_insert(Subject subject, int number, char teacher[1024], int credit_hours);
int duplicate_class(Subject subject, int number, char teacher[1024], int credit_hours);
void schedule_print();
void course_drop(Subject subject, int number);
void schedule_load();
void schedule_save();
int file_exists(char string[]);

//main entry point. Starts the program by displaying a welcome and beginning an 
//input loop that displays a menu and processes user input. Pressing q quits.      
int main_stuff() {
    schedule_load();

	char input_buffer;

	printf("\n\nWelcome to ASU Class Schedule\n");

	//TODO: stuff goes here...

	//menu and input loop
	do {
		printf("\nMenu Options\n");
		printf("------------------------------------------------------\n");
		printf("a: Add a class\n");
		printf("d: Drop a class\n");
		printf("s: Show your classes\n");
		printf("q: Quit\n");
		printf("\nTotal Credits: %d\n\n", getCreditCount());
		printf("Please enter a choice ---> ");

		scanf(" %c", &input_buffer);

		branching(input_buffer);
	} while (input_buffer != 'q');

	//TODO: stuff goes here...

	return 0;
}

//takes a character representing an inputs menu choice and calls the appropriate
//function to fulfill that choice. display an error message if the character is
//not recognized.
void branching(char option) {
	switch (option) {
        case 'a': {
            Subject subject;
            int number;
            char teacher[1024];
            int credit_hours;
            int temp;

            printf("What is the subject? (SER=0, EGR=1, CSE=2, EEE=3)\n");
            scanf("%d", &temp);
            switch (temp) {
                case 0:
                    subject = SER;
                    break;
                case 1:
                    subject = EGR;
                    break;
                case 2:
                    subject = CSE;
                    break;
                case 3:
                    subject = EEE;
                    break;
            }

            printf("What is the number (e.g. 240)?\n");
            scanf("%d", &number);

            printf("How many credits is the class (e.g. 3)?\n");
            scanf("%d", &credit_hours);

            printf("What is the name of the teacher?\n");
            scanf("%s", teacher);


            if (!duplicate_class(subject, number, teacher, credit_hours)) {
                course_insert(subject, number, teacher, credit_hours);
            } else {
                printf("No duplicate classes allowed!\n");
            }
            break;
        }

        case 'd': {
            Subject subject;
            int number;
            int temp;

            printf("Removing class...\n");
            printf("What is the subject? (SER=0, EGR=1, CSE=2, EEE=3)\n");
            scanf("%d", &temp);
            switch (temp) {
                case 0:
                    subject = SER;
                    break;
                case 1:
                    subject = EGR;
                    break;
                case 2:
                    subject = CSE;
                    break;
                case 3:
                    subject = EEE;
                    break;
            }

            printf("Enter Number:\n");
            scanf("%d", &number);

            course_drop(subject, number);
            break;
        }

        case 's': {
            schedule_print();
            break;
        }

        case 'q': {
            schedule_save();

            CourseNode *node = course_collection;
            while (node != NULL) {
                CourseNode *tmp = node;
                node = node->next;
                free(tmp);
            }
            // main loop will take care of this.
            break;
        }

        default: {
            printf("\nError: Invalid Input.  Please try again...");
            break;
        }
	}
}

int getCreditCount(){
    CourseNode* node = course_collection;
    int count = 0;
    while(node != NULL){
        count += node->credit_hours;
        node = node->next;
    }
    return count;
}

void course_insert(Subject subject, int number, char teacher[1024], int credit_hours){
    CourseNode* newNode = malloc(sizeof(CourseNode));
    newNode->subject = subject;
    newNode->number = number;
    strcpy(newNode->teacher, teacher);
    newNode->credit_hours = credit_hours;
    newNode->next == NULL;

    if(course_collection == NULL){
        course_collection = newNode;
    }
    else{
        if(newNode->subject < course_collection->subject || (newNode->subject == course_collection->subject && newNode->number < course_collection->number)){
            newNode->next = course_collection;
            course_collection = newNode;
        }
        else {
            CourseNode* node = course_collection;
            while (node->next != NULL) {
                if (newNode->subject < node->next->subject || (newNode->subject == node->next->subject && newNode->number < node->next->number)) {
                    break;
                }
                node = node->next;
            }
            newNode->next = node->next;
            node->next = newNode;
        }
    }
}

int duplicate_class(Subject subject, int number, char teacher[1024], int credit_hours){
    CourseNode* node = course_collection;
    while(node != NULL){
        if(subject == node ->subject && number == node->number){
            return 1;
        }
        node = node->next;
    }
    return 0;
}

void schedule_print(){
    printf("Class Schedule:\n");
    CourseNode* node = course_collection;
    while(node != NULL){
        printf("%s%d  %d  %s\n", subjectStrings[node->subject], node->number, node->credit_hours, node->teacher);
        node = node->next;
    }
}

void course_drop(Subject subject, int number){
    if(course_collection == NULL){
        return;
    }
    if(course_collection->subject == subject && course_collection->number == number){
        CourseNode* tmp = course_collection->next;
        free(course_collection);
        course_collection = tmp;
    }
    CourseNode* node = course_collection;
    while(node->next != NULL){
        if(node->next->subject == subject && node->next->number == number){
            CourseNode* tmp = node->next;
            node->next = node->next->next;
            free(tmp);
            break;
        }
        node = node->next;
    }
}

void schedule_save(){
    FILE *f;
    f = fopen("./schedule_data.txt", "w");
    CourseNode* node = course_collection;
    while(node != NULL){
        fwrite(node, sizeof (CourseNode), 1, f);
        //fprintf(f, "%d %d %d %s\n", node->subject, node->number, node->credit_hours, node->teacher);
        node = node->next;
    }
    fclose(f);
}

void schedule_load(){
    if(file_exists("./schedule_data.txt")) {
        printf("Found savefile; loading...\n");
        FILE *f;
        f = fopen("./schedule_data.txt", "r");
        CourseNode *buf = malloc(sizeof(CourseNode));
        CourseNode *node = buf;
        CourseNode *head = node;
        while(fread(buf, sizeof(CourseNode), 1, f) == 1){
            buf = malloc(sizeof(CourseNode));
            node->next = buf;
            node = node->next;
        }
        fclose(f);

        //ugly band-aid I know, but I'm tired of staring at this trying to figure out how to solve it properly, so we're doing this instead.
        node = head;
        while(node->next->next != NULL){
            node = node->next;
        }

        node->next = NULL;
        free(buf);

        course_collection = head;
    }
    else{
        printf("Did not find savefile.\n");
    }
}

int file_exists(char string[]){
    FILE *f;
    if((f = fopen(string, "r"))){
        fclose(f);
        return 1;
    }
    return 0;
}

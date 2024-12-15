#ifndef BINTREE_H
#define BINTREE_H

// Node structure should have an int node_id, an int data, and pointers to left and right child nodes

typedef struct node {
    int node_id;
    int data;
    struct node *right;
    struct node *left;
} node;

///*** DO NOT CHANGE ANY FUNCTION DEFINITIONS ***///
void insert_node(int node_id, int data);
int find_node_data(int node_id);
#endif

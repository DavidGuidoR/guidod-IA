#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define epoca 300000
#define K 0.03f

// Declaración de funciones
float EntNt_AND(float, float, float);
float EntNt_OR(float, float, float);
float EntNt_XOR(float, float, float);
float InitNt_AND(float, float);
float InitNt_OR(float, float);
float InitNt_XOR(float, float);
float sigmoide(float);
void pesos_initNt_AND();
void pesos_initNt_OR();
void pesos_initNt_XOR();

// Pesos y bias para compuerta AND
float Pesos_AND[2];
float bias_AND = 0.5f;
float Error_AND;

// Pesos y bias para compuerta OR
float Pesos_OR[2];
float bias_OR = 0.5f;
float Error_OR;

// Pesos y bias para perceptrón XOR (entrenado con salidas de AND y OR)
float Pesos_XOR[2];
float bias_XOR = 0.5f;
float Error_XOR;

// Función de entrenamiento para compuerta AND
float EntNt_AND(float x0, float x1, float target) {
    float net = Pesos_AND[0] * x0 + Pesos_AND[1] * x1 - bias_AND;
    net = sigmoide(net);

    Error_AND = target - net;
    bias_AND -= K * Error_AND;

    float delta[2];
    delta[0] = K * Error_AND * x0;
    delta[1] = K * Error_AND * x1;

    Pesos_AND[0] += delta[0];
    Pesos_AND[1] += delta[1];

    return net;
}

// Función de entrenamiento para compuerta OR
float EntNt_OR(float x0, float x1, float target) {
    float net = Pesos_OR[0] * x0 + Pesos_OR[1] * x1 - bias_OR;
    net = sigmoide(net);

    Error_OR = target - net;
    bias_OR -= K * Error_OR;

    float delta[2];
    delta[0] = K * Error_OR * x0;
    delta[1] = K * Error_OR * x1;

    Pesos_OR[0] += delta[0];
    Pesos_OR[1] += delta[1];

    return net;
}

// Función de entrenamiento para el perceptrón XOR
float EntNt_XOR(float x0, float x1, float target) {
    float net = Pesos_XOR[0] * x0 + Pesos_XOR[1] * x1 - bias_XOR;
    net = sigmoide(net);

    Error_XOR = target - net;
    bias_XOR -= K * Error_XOR;

    float delta[2];
    delta[0] = K * Error_XOR * x0;
    delta[1] = K * Error_XOR * x1;

    Pesos_XOR[0] += delta[0];
    Pesos_XOR[1] += delta[1];

    return net;
}

float sigmoide(float s) {
    return (1 / (1 + exp(-s)));
}

void pesos_initNt_AND() {
    for (int i = 0; i < 2; i++) {
        Pesos_AND[i] = (float)rand() / RAND_MAX;
    }
}

void pesos_initNt_OR() {
    for (int i = 0; i < 2; i++) {
        Pesos_OR[i] = (float)rand() / RAND_MAX;
    }
}

void pesos_initNt_XOR() {
    for (int i = 0; i < 2; i++) {
        Pesos_XOR[i] = (float)rand() / RAND_MAX;
    }
}

int main() {
    int i = 0;
    float apr_AND, apr_OR, apr_XOR;

    // Inicializar pesos para AND, OR y XOR
    pesos_initNt_AND();
    pesos_initNt_OR();
    pesos_initNt_XOR();

    while (i < epoca) {
        printf("------------------------\n");
        printf("Salida Entrenamiento Epoca %d (Compuertas AND, OR y XOR)\n", i);

        // Entrenamiento compuerta AND
        apr_AND = EntNt_AND(1, 1, 1);
        apr_OR = EntNt_OR(1, 1, 1);
        apr_XOR = EntNt_XOR(apr_AND, apr_OR, 0); // XOR 1,1 = 0
        printf("XOR (AND=1, OR=1) = %f\n", apr_XOR);

        apr_AND = EntNt_AND(1, 0, 0);
        apr_OR = EntNt_OR(1, 0, 1);
        apr_XOR = EntNt_XOR(apr_AND, apr_OR, 1); // XOR 1,0 = 1
        printf("XOR (AND=0, OR=1) = %f\n", apr_XOR);

        apr_AND = EntNt_AND(0, 1, 0);
        apr_OR = EntNt_OR(0, 1, 1);
        apr_XOR = EntNt_XOR(apr_AND, apr_OR, 1); // XOR 0,1 = 1
        printf("XOR (AND=0, OR=1) = %f\n", apr_XOR);

        apr_AND = EntNt_AND(0, 0, 0);
        apr_OR = EntNt_OR(0, 0, 0);
        apr_XOR = EntNt_XOR(apr_AND, apr_OR, 0); // XOR 0,0 = 0
        printf("XOR (AND=0, OR=0) = %f\n", apr_XOR);

        printf("Pesos XOR en cada epoca\n");
        printf("Peso XOR 0 = %f\n", Pesos_XOR[0]);
        printf("Peso XOR 1 = %f\n", Pesos_XOR[1]);
        printf("Bias XOR = %f\n", bias_XOR);
        printf("Error XOR = %f\n", Error_XOR);

        printf("------------------------\n");

        i++;
    }

    return 0;
}

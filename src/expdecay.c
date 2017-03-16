#include <stdio.h>
#include <math.h>
#include <string.h>
#include <time.h>

#define MAXITER 1000000
#define MAXLEN 16
#define BUFLEN (MAXLEN+2)   // 1 excess char, and '\0'.

static volatile double x = 0.5;
static volatile double lambda = 1.0;

static void timeit(const char *fname, double (*fun)());
static double expdecay();
static double expdecay2();
static double time_expdecay2();
__attribute__((noinline)) static double expdecay2();
static void fixlen(char *buf, const char *s);


int main(int argc, char *argv[]) {
    timeit("expdecay", &expdecay);
    timeit("time_expdecay2", &time_expdecay2);

    return 0;
}


static void timeit(const char *fname, double (*fun)()) {
    char fixed_fname[BUFLEN];
    char lang[BUFLEN];
    double latency;     // In us (microseconds).
    struct timespec start, end, temp;
    double y;

    clock_gettime(CLOCK_REALTIME, &start);
    y = (*fun)();
    clock_gettime(CLOCK_REALTIME, &end);
    latency = start.tv_sec;

    //See: http://www.guyrutenberg.com/2007/09/22/profiling-code-using-clock_gettime/
    if ((end.tv_nsec-start.tv_nsec)<0) {
        temp.tv_sec = end.tv_sec-start.tv_sec-1;
        temp.tv_nsec = 1000000000+end.tv_nsec-start.tv_nsec;
    } else {
        temp.tv_sec = end.tv_sec-start.tv_sec;
        temp.tv_nsec = end.tv_nsec-start.tv_nsec;
    }
    latency = ((((double)temp.tv_sec)*1000000.0
                    + ((double)temp.tv_nsec)/1000.0) / MAXITER);

    fixlen(lang, "C");
    //fixlen(lang, "0123456789abcdefxyzd");     // Rudimentary unit test :)
    fixlen(fixed_fname, fname);
    printf("%s\t%s\t%.1lf mtps\t%.2lf us/txn\n", lang, fixed_fname,
            1.0/latency, latency);
}

static double expdecay() {
    double y;
    for (int i=0; i < MAXITER; i++)
        y = exp(-lambda*x);
    return y;
}

static double time_expdecay2() {
    double y;
    for (int i=0; i < MAXITER; i++)
        y = expdecay2();
    return y;
}

static double expdecay2() {
    return exp(-lambda*x);
}

static void fixlen(char *buf, const char *s) {
    int srclen;

    strncpy(buf, s, BUFLEN);
    srclen = strnlen(buf, BUFLEN-1);
    if (srclen <= MAXLEN) {
        // Right pad with white spaces
        for (int i=srclen; i < BUFLEN-1; i++)
            buf[i] = ' ';
        buf[BUFLEN-1] = '\0';
    } else {
        // Mangle as "xxx..." (NOTE: loop unrolling)
        buf[MAXLEN-3] = buf[MAXLEN-2] = buf[MAXLEN-1] = '.';
        buf[MAXLEN] = '\0';
    }
}

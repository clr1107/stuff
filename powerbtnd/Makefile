CC ?= gcc
CFLAGS ?= -I. -Wall -Wextra -O3

POWERBTND_SRCS = powerbtnd.o

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

all: powerbtnd

powerbtnd: $(POWERBTND_SRCS)
	$(CC) $(CFLAGS) -o $@ $(POWERBTND_SRCS)

.PHONY: all

clean:
	rm -rf $(POWERBTND_SRCS)

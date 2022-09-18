#define _GNU_SOURCE

#include <stdlib.h>
#include <errno.h>
#include <linux/input.h>
#include <string.h>
#include <stdio.h>
#include <linux/limits.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

enum powerbtnd_err {
	POWERBTND_OS,
	POWERBTND_ERR_OPEN_FILE,
	POWERBTND_ERR_SHUTDOWN_FAIL,
};

static const char *powerbtnd_err_s[] = {
		"OS",
		"could not open file",
		"failed to shutdown"
};

struct powerbtnd_ret {
	int error;
	char *error_s;
};

// callback function for when the power button is pressed.
int powerbtnd_key_power(void);

int main(int argc, char **argv)
{
	char dev_input_file[PATH_MAX] = "/dev/input/event1";
	struct powerbtnd_ret ret = {.error=0};

	if (argc > 1)
		strncpy(dev_input_file, argv[1], PATH_MAX-1);

	fprintf(stdout, "using path %s\n", dev_input_file);

	int fd;
	if ((fd = open(dev_input_file, O_RDONLY)) == -1) {
		ret.error = POWERBTND_ERR_OPEN_FILE;
		asprintf(&ret.error_s, "device file %s", dev_input_file);

		goto exit;
	}

	struct input_event ev;
	ssize_t n;

	for (;;) {
		n = read(fd, &ev, sizeof ev);

		if ((n == (ssize_t) - 1 && errno != EINTR) || (n != sizeof ev)) {
			ret.error = POWERBTND_OS;
			asprintf(&ret.error_s, "err: (%d) %s", errno, strerror(errno));

			goto exit;
		}

		if (ev.type == EV_KEY && ev.value >= 0 && ev.value <= 2) {
			if (ev.code == KEY_POWER) {
				fprintf(stdout, "button pressed; shutting down\n");

				int code;
				if ((code = powerbtnd_key_power())) {
					ret.error = POWERBTND_ERR_SHUTDOWN_FAIL;
					asprintf(&ret.error_s, "exit code: %d", code);
				}

				goto exit;
			}
		}
	}

	exit:
	if (ret.error) {
		fflush(stdout);
		fprintf(stderr, "error (%d): %s: %s\n", ret.error, powerbtnd_err_s[ret.error], ret.error_s);

		free(ret.error_s);
	}

	return ret.error;
}

int powerbtnd_key_power(void)
{
        // do something now that the power button has been pressed.
	return system(
			"/usr/sbin/shutdown -P +1 '(Via powerbtnd.)' && echo \"Shutting down at $(date +\"%H:%M\") via powerbtnd\" | clrauto.sh"
        );
}

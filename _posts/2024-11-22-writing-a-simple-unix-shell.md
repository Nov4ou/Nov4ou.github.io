---
layout: post
title: Write a Simple UNIX Shell Using C
categories:
- UNIX Programming
tags:
- CSAPP
date: '2024-11-22 16:08:51 +0800'
---
A UNIX shell is essentially an interactive program that runs other programs on behalf of the user. 

> A Unix shell is a command-line interpreter or shell that provides a command line user interface for Unix-like operating systems. The shell is both an interactive command language and a scripting language, and is used by the operating system to control the execution of the system using shell scripts.
>
> — [Wikipedia](https://en.wikipedia.org/wiki/Unix_shell)

Using the `fork` and `execve` C functions, we can create a simple shell program. The
 `fork` function creates a child process while the `execve` function loads and runs the desired program along with its arguments specified by the user’s input. The user‘s command runs in the child process. Once the child process finishes execution, it is reaped and control returns to the parent process, allowing the shell to wait for the next user input.

## The main routine
The main routine is straightforward: it displays a `>` command-line prompt and waits for the user to type a command on `stdin`. The entered command is then processed by the `eval` routine.

```c
int main() {
  char cmdline[MAXLINE]; /* Command line */

  while (1) {
    /* Read */
    printf("> ");
    Fgets(cmdline, MAXLINE, stdin);
    if (feof(stdin)) exit(0);

    /* Evaluate */
    eval(cmdline);
  }
}
```

The `feof(stdin)` is used to check whether the end-of-file (EOF) condition has been reached for the stdin stream.

## The eval routine

```c
/* eval - Evaluate a command line */
void eval(char *cmdline) {
  char *argv[MAXARGS]; /* Argument list execve() */
  char buf[MAXLINE];   /* Holds modified command line */
  int bg;              /* Should the job run in bg or fg? */
  pid_t pid;           /* Process id */

  strcpy(buf, cmdline);
  bg = parseline(buf, argv);
  if (argv[0] == NULL) return; /* Ignore empty lines */

  if (!builtin_command(argv)) {
    if ((pid = Fork()) == 0) { /* Child runs user job */
      if (execvp(argv[0], argv) < 0) {
        perror("execvp error");
        exit(0);
      }

      // if (execve(argv[0], argv, environ) < 0) {
      //   printf("%s: Command not found.\n", argv[0]);
      //   exit(0);
      // }

    }

    /* Parent waits for foreground job to terminate */
    if (!bg) {
      int status;
      if (waitpid(pid, &status, 0) < 0) unix_error("waitfg: waitpid error");
    } else
      printf("%d %s", pid, cmdline);
  }
  return;
}
```

> Note: The `execev` function does not automatically resolve the PATH environment variable, so you must ues the absolute path, such as `/bin/ls`. If you want to execute commands by simply typing the command name (e.g., ls) like in a regular shell, you can use the `execvp` function, which automatically resolves PATH.
{: .prompt-tip }

## The praseline routine

The `parseline` function parses the space-separated command-line arguments and constructs the `argv` vector, which is then passed to `execve`.
```c
/* parseline - Parse the command line and build the argv array */
int parseline(char *buf, char **argv) {
  char *delim; /* Points to first space delimiter */
  int argc;    /* Number of args */
  int bg;      /* Background job? */

  buf[strlen(buf) - 1] = ' ';   /* Replace trailing '\n' with space */
  while (*buf && (*buf == ' ')) /* Ignore leading spaces */
    buf++;

  /* Build the argv list */
  argc = 0;
  while ((delim = strchr(buf, ' '))) {
    argv[argc++] = buf;
    *delim = '\0';
    buf = delim + 1;
    while (*buf && (*buf == ' ')) /* Ignore spaces */
      buf++;
  }
  argv[argc] = NULL;

  if (argc == 0) /* Ignore blank line */
    return 1;

  /* Should the job run in the background? */
  if ((bg = (*argv[argc - 1] == '&')) != 0) argv[--argc] = NULL;

  return bg;
}
```

## Build and run the project
The complete project is available on the [GitHub repo](https://github.com/Nov4ou/csapp_test/tree/main/chapter-8/shell).

To build this project, navigate to the project directory and run:
```shell
make
```
Then execute the `main` program:
```shell
./main  
```

Since we use `execvp()` instead of `execve()`, you can simply type the command name, such as ls:
```shell
ls
```
Here is the result:
![Desktop View](/assets/img/shell/Screenshot 2024-11-22 at 15.56.45.png){: width="972" height="589" }

You can also try system-level commands like `sudo apt update` and `sudo apt upgrade`:
![Desktop View](/assets/img/shell/Screenshot 2024-11-22 at 16.01.15.png){: width="972" height="589" }

> Note: You can't use the combined command `sudo apt update && sudo apt upgrade` nor can you use the up arrow key to view previously typed commands. These functionalities are implemented by shells like `bash` or `zsh`.
{: .prompt-info }





<!-- <script src="https://utteranc.es/client.js"
        repo="Nov4ou/Nov4ou.github.io"
        issue-term="pathname"
        theme="github-dark"
        crossorigin="anonymous"
        async>
</script> -->


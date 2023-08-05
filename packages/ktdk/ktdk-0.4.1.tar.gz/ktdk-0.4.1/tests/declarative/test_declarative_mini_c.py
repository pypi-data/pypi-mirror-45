HELLO_DEF = """
config:
    timeout: 20

suite:
    name: hello
    description: Hello world intro program
    tasks:
        - fs:
              tool: copy
              submission:
                  - 'hello.c'
              test_files:
                  - pattern: 'solution.c'
        - build:
            tool: c_raw
            executable: student_hello
            files:
                - hello.c
            required: true
        - build:
            tool: c_raw
            executable: teacher_hello
            files:
                - solution.c
            required: true
    tests:
        - name: student_hello
          description: Student's hello should write hello
          tags:
            - naostro
          tasks:
            - execute:
                executable: student_hello
                executor: valgrind
                checks:
                    - type: stdout
                      regex: 'Hello World!'
                    - type: stderr
                      equals: ''
                    - type: return_code
                      equals: 0
"""

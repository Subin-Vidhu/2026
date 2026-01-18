Video refered - [Link](https://youtu.be/XmpIBsnc3xU?si=y98rGTUY3eyfMK43)

- Debugging in VS Code

    - Open the folder in VS Code
    - Go to the Run and Debug section (Ctrl + Shift + D)
    - Click on "create a launch.json file"
    - Select "Debug Python File"
    - This will create a launch.json file with default configurations
    - You can modify the configurations as needed
    - To start debugging, set breakpoints in your code by clicking on the left margin next to the line numbers

        - Types of Breakpoints:
            - Standard Breakpoint: Click on the left margin next to the line number, default behavior
            - Conditional Breakpoint: Right-click on the breakpoint and select "Edit Breakpoint" to add a condition, such as pausing only when a variable reaches a certain value, eg. `if name == "John"`
            - Logpoint: Right-click on the breakpoint and select "Convert to Logpoint" to log a message instead of stopping execution, eg. `Value of x is {x}`
            - Hit Count Breakpoint: Right-click on the breakpoint and select "Edit Breakpoint" to specify how many times it should be hit before pausing execution, eg. `Hit count is 5`
            - Function Breakpoint: Use the "Breakpoints" section in the Run and Debug sidebar to add a breakpoint that pauses execution when a specific function is called, eg. `my_function`
    - Click on the green play button in the Run and Debug section or press F5 to start debugging
    - Use the debugging toolbar to step through the code, continue execution, or stop debugging as needed   
    - You can inspect variables, view the call stack, and evaluate expressions in the Debug Console
    - To stop debugging, click on the red square button in the debugging toolbar or press Shift + F5    

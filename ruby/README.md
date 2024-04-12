# Lol Module

The Lol module is a Ruby script designed to enhance terminal output with vibrant rainbow colors, offering options for both static and animated text display. It utilizes the `lolcat` and `paint` gems to create engaging visual effects in the terminal, suitable for both development fun and enhancing CLI tool output readability.

## Features

- **Rainbow Coloring**: Apply a continuous spectrum of colors to text.
- **Animation**: Animate the display of text with moving colors.
- **Customizable Options**: Control the frequency, speed, and intensity of the animations and colors.

## Installation

1. Clone the Repository:
   ```
   git clone https://github.com/yourusername/lol-module.git
   cd lol-module
   ```

2. Install Dependencies:
   - Ensure Ruby is installed on your system.
   - Install required Ruby gems:
     ```
     gem install lolcat paint
     ```

## Usage

### Basic Usage

To use the Lol module, include it in your Ruby scripts:

```ruby
require_relative 'path/to/lol'

# Example of using the module
Lol.println("Hello, world!", {freq: 0.3, spread: 3, speed: 10, duration: 5, os: 0}, animate: true)
```

### Advanced Usage - Terminal Output Hijack

You can use the Lol module to hijack the output of your terminal session and apply rainbow effects to all displayed text:

1. Create a Ruby script (`rainbow_output.rb`):
   ```ruby
   require_relative 'lol'

   while line = gets
     Lol.println(line, {freq: 0.3, spread: 3, speed: 10, duration: 5, os: 0}, animate: false)
   end
   ```

2. Run the Script with Terminal Output:
   - Use this command to see the output of any command in rainbow colors:
     ```
     ls -l | ruby rainbow_output.rb
     ```
     Tail syslog
     ```
    tail -f /var/log/syslog | ruby rainbow-output.rb 
    ```
   - To continuously colorise terminal output:
     ```
     script -q /dev/null | ruby rainbow_output.rb
     ```
     To open a new terminal to continuously colorise terminal output
    ```
     xfce4-terminal -e "bash -c 'script -q /dev/null | ruby rainbow-output.rb; exec bash'"
    ```

## Examples

- Static Text:
  ```ruby
  Lol.println("Static rainbow text", {freq: 0.1, spread: 2, os: 0}, animate: false)
  ```

- Animated Text:
  ```ruby
  Lol.println("Animated rainbow text", {freq: 0.3, spread: 3, speed: 10, duration: 10, os: 0}, animate: true)
  ```

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
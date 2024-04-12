require_relative 'lol'  # Adjust this path if your files are structured differently

# Example usage of the Lol module
messages = ["Hello, world!", "Welcome to the colorful terminal!", "Enjoy the animations!"]
options = { animate: true, freq: 0.1, spread: 3, speed: 10, duration: 5, os: 0 }

# Run the animation and color effects on each message
messages.each do |message|
  puts "Displaying: #{message}"
  Lol.cat([message], options)
  sleep 2  # Pause between messages to make them distinguishable
end

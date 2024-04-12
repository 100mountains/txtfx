# rainbow_filter.rb
require_relative 'lol'

def apply_rainbow
  ARGF.each_line do |line|
    Lol.println(line, {freq: 0.3, spread: 3, speed: 10, os: 0}, animate: false)
  end
end

apply_rainbow

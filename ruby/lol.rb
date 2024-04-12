require "lolcat/version"
require 'paint'

module Lol
  STRIP_ANSI = Regexp.compile '\e\[(\d+)(;\d+)?(;\d+)?[m|K]', nil

  def self.rainbow(freq, i)
    red   = Math.sin(freq*i + 0) * 127 + 128
    green = Math.sin(freq*i + 2*Math::PI/3) * 127 + 128
    blue  = Math.sin(freq*i + 4*Math::PI/3) * 127 + 128
    "#%02X%02X%02X" % [ red, green, blue ]
  end

  def self.cat(fd, opts={})
    print "\e[?25l" if opts[:animate]
    fd.each do |line|
      opts[:os] = opts[:os] ? opts[:os] + 1 : 1
      println(line, opts)
    end
  ensure
    print "\e[?25h" if opts[:animate]
  end

  def self.println(str, defaults={}, opts={})
    STDOUT.sync = true  # Ensure that each line is output immediately
    opts = defaults.merge(opts)
    str.chomp!
    str.gsub! STRIP_ANSI, ''
    if opts[:animate]
      println_ani(str, opts)
    else
      println_plain(str, opts)
    end
    puts  # Ensure a newline is added after each processed line
  end

  private

  def self.println_plain(str, defaults={}, opts={})
    opts = defaults.merge(opts)
    str.chars.each_with_index do |c, i|
      print Paint[c, rainbow(opts[:freq], opts[:os]+i/opts[:spread])]
    end
  end

  def self.println_ani(str, opts={})
    return if str.empty?
    (1..opts[:duration]).each do |i|
      print "\e[#{str.length}D"
      opts[:os] += opts[:spread]
      println_plain(str, opts)
      sleep 1.0/opts[:speed]
    end
  end
end

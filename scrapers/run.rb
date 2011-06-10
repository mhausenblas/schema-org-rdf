#!/usr/bin/ruby

def check_lines(file, expected)
    output = `wc -l #{file}`
    abort "#{file} was not created. Aborting!" if !output
    abort "wc -l failed on #{file}. Aborting!" unless m = /\d+/.match(output)
    abort "#{file} has less than #{expected} lines (#{m[0]}. Aborting!" if m[0].to_i < expected
end

abort "Usage: run.rb tmp_dir target_dir" if ARGV.length != 2
puts Time.now
tmp_dir = ARGV[0]
target_dir = ARGV[1]
files = ['all-classes.csv', 'all-properties.csv', 'all.json', 'all.ttl', 'all.nt', 'all.rdf']
files.each { |f| `rm #{tmp_dir}/#{f} 2> /dev/null` }
`python scrape_csv.py #{tmp_dir}/all-classes.csv #{tmp_dir}/all-properties.csv`
`python scrape_json.py > #{tmp_dir}/all.json`
`python scrape_rdf.py > #{tmp_dir}/all.ttl`
`any23 -f ntriples #{tmp_dir}/all.ttl > #{tmp_dir}/all.nt`
`any23 -f rdfxml #{tmp_dir}/all.ttl > #{tmp_dir}/all.rdf`
check_lines("#{tmp_dir}/all-classes.csv", 100)
check_lines("#{tmp_dir}/all-properties.csv", 100)
check_lines("#{tmp_dir}/all.json", 10000)
check_lines("#{tmp_dir}/all.ttl", 2000)
check_lines("#{tmp_dir}/all.nt", 2000)
check_lines("#{tmp_dir}/all.rdf", 2000)
files.each { |f| `cp #{tmp_dir}/#{f} #{target_dir}/#{f}` }

python cluster.py -k 1 -i forgy -e 1 -o image_centroids_1.csv image_data.csv
python cluster.py -k 4 -i forgy -e 1 -o image_centroids_4.csv image_data.csv
python cluster.py -k 8 -i forgy -e 1 -o image_centroids_8.csv image_data.csv
python cluster.py -k 16 -i forgy -e 1 -o image_centroids_16.csv image_data.csv
python cluster.py -k 32 -i forgy -e 1 -o image_centroids_32.csv image_data.csv
python cluster.py -k 64 -i forgy -e 1 -o image_centroids_64.csv image_data.csv

python image.py compress -o compressed_1.pgm images/tiger.ppm image_centroids_1.csv
python image.py compress -o compressed_4.pgm images/tiger.ppm image_centroids_4.csv
python image.py compress -o compressed_8.pgm images/tiger.ppm image_centroids_8.csv
python image.py compress -o compressed_16.pgm images/tiger.ppm image_centroids_16.csv
python image.py compress -o compressed_32.pgm images/tiger.ppm image_centroids_32.csv
python image.py compress -o compressed_64.pgm images/tiger.ppm image_centroids_64.csv

python image.py decompress -o tiger_decompressed_1.ppm compressed_1.pgm image_centroids_1.csv
python image.py decompress -o tiger_decompressed_4.ppm compressed_4.pgm image_centroids_4.csv
python image.py decompress -o tiger_decompressed_8.ppm compressed_8.pgm image_centroids_8.csv
python image.py decompress -o tiger_decompressed_16.ppm compressed_16.pgm image_centroids_16.csv
python image.py decompress -o tiger_decompressed_32.ppm compressed_32.pgm image_centroids_32.csv
python image.py decompress -o tiger_decompressed_64.ppm compressed_64.pgm image_centroids_64.csv

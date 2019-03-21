if [ "$#" -ne 2 ]; then
	python3 encodeMaze.py $1 1
else
	python3 encodeMaze.py $1 $2
fi
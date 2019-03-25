if [ "$#" -ne 3 ]; then
	python3 runPolicy.py $1 $2
else
	python3 runPolicy.py $1 $2 $3
fi
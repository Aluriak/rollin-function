while true; do
    python main.py | shuf -n 1 > out.txt
    cat out.txt
    cat out.txt | espeak -v fr-fr -s 150 &> /dev/null
    sleep 1
done

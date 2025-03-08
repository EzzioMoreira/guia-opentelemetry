while true ; do
    livro_id=$((RANDOM % 200 + 1))  # Gera IDs entre 1 e 1000
    echo "Gerando carga para livro ID: $livro_id..."
    curl -X 'POST' \
    'http://localhost:8081/ordens/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
      "id_livro": '"$livro_id"'
    }'
    sleep 1
done
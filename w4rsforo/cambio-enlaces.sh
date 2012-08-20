grep -rl "foro.w4rs.com" * | xargs sed -i -e 's/localhost:8000/foro.w4rs.com/'

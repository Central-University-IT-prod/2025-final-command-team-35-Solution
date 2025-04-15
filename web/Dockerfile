# Stage 1: Build
FROM oven/bun:latest AS build
WORKDIR /app
COPY package.json .
COPY bun.lock .
RUN bun install --frozen-lockfile
COPY . .
RUN bun run build

# Проверка содержимого директории после сборки
RUN ls -la /app/build

# Stage 2: Run
FROM nginx:alpine

# Удаление стандартного содержимого директории html, но не всей директории nginx
RUN rm -rf /usr/share/nginx/html/*

# Копирование собранного приложения из этапа сборки
COPY --from=build /app/build /usr/share/nginx/html

# Копирование пользовательской конфигурации Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Установка прав на директорию
RUN chown -R nginx:nginx /usr/share/nginx/html
RUN chmod -R 755 /usr/share/nginx/html

# Экспозиция порта 80
EXPOSE 80

# Запуск Nginx
CMD [ "nginx", "-g", "daemon off;" ]
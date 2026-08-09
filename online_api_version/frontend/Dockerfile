# 阶段一：构建阶段
FROM node:16-alpine AS build

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制所有文件并构建应用
COPY . .
RUN npm run build

# 阶段二：生产阶段
FROM nginx:stable-alpine

# 复制构建产物到 Nginx 的 html 目录
COPY --from=build /app/dist /usr/share/nginx/html

# 复制自定义的 Nginx 配置（如果需要）
COPY nginx.conf /etc/nginx/nginx.conf

# 暴露端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]

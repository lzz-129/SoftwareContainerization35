# 使用 Node 官方镜像作为基础镜像
FROM node:latest as build-stage

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json 文件
COPY package*.json ./

# 安装项目依赖
RUN npm install

# 复制项目文件到工作目录
COPY . .

# 构建应用
RUN npm run build

# 为生产环境使用 Nginx
FROM nginx:stable-alpine as production-stage

# 从构建阶段复制构建出的文件到 Nginx 的目录下
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 暴露 80 端口
EXPOSE 80

# 当容器启动时，运行 Nginx
CMD ["nginx", "-g", "daemon off;"]
# Multi-stage build for SvelteKit app
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN npm i --silent || true
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/build ./build
RUN npm i --omit=dev --silent || true
EXPOSE 3000
CMD ["node", "./build"]

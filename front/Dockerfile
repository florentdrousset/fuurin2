# Multi-stage build for SvelteKit app
FROM node:20-alpine AS builder
WORKDIR /app
# Ensure devDependencies are installed during build
ENV NODE_ENV=development
ENV NPM_CONFIG_PRODUCTION=false
# Copy only package.json to avoid inheriting stale lockfiles from host
COPY package.json ./
# Install all deps including dev to ensure svelte-kit CLI is available
RUN npm install --include=dev --legacy-peer-deps && node -e "console.log('@sveltejs/kit', require('./node_modules/@sveltejs/kit/package.json').version)"
# Now copy the rest of the project
COPY . .
# Diagnostic: ensure kit and config resolve in the project dir
RUN node -e "console.log('kit:', require.resolve('@sveltejs/kit/package.json')); console.log('adapter-auto:', require.resolve('@sveltejs/adapter-auto/package.json')); require('./svelte.config.js'); console.log('config OK')"
# Extra diagnostics to understand CLI resolution
RUN node -e "const p=require('./node_modules/@sveltejs/kit/package.json'); console.log('kit bin field:', p.bin); console.log('kit version:', p.version)"
RUN sh -lc "set -x; ls -l ./node_modules/.bin/svelte-kit; head -n 5 ./node_modules/.bin/svelte-kit || true"
# Build via npm script (uses local svelte-kit)
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
# Copy built app
COPY --from=builder /app/build ./build
# Start the built server
# We use adapter-node to produce a Node server at build/index.js
EXPOSE 3000
CMD ["node", "./build/index.js"]

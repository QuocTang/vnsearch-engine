#!/usr/bin/env bash

# ==============================================================================
# Build & Push Docker Images to Docker Hub
# Services: irs_api, irs_web
# ==============================================================================

set -eo pipefail

# ── Configuration ─────────────────────────────────────────────────────────────
DOCKER_HUB_USERNAME="${DOCKER_HUB_USERNAME:-quoctang}"  # Thay bằng username Docker Hub của bạn
IMAGE_PREFIX="${IMAGE_PREFIX:-vnsearch}"                 # Prefix cho tên image
VERSION="${VERSION:-latest}"                             # Tag version, mặc định là "latest"

# Thư mục gốc của project (1 cấp trên thư mục deploy/)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Danh sách services cần build (name:context_path)
ALL_SERVICES="irs_api irs_web"

get_context_dir() {
    local service_name="$1"
    echo "${PROJECT_ROOT}/microservices/${service_name}"
}

# ── Colors & Helpers ──────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

info()    { echo -e "${BLUE}[INFO]${NC}    $*"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}    $*"; }
error()   { echo -e "${RED}[ERROR]${NC}   $*"; }

separator() {
    echo -e "${CYAN}──────────────────────────────────────────────────────────${NC}"
}

# ── Usage ─────────────────────────────────────────────────────────────────────
usage() {
    echo ""
    echo "Usage: $0 [OPTIONS] [SERVICES...]"
    echo ""
    echo "Build và push Docker images lên Docker Hub."
    echo ""
    echo "Options:"
    echo "  -u, --username USERNAME   Docker Hub username (mặc định: ${DOCKER_HUB_USERNAME})"
    echo "  -v, --version  VERSION    Image tag/version  (mặc định: ${VERSION})"
    echo "  -p, --prefix   PREFIX     Image name prefix  (mặc định: ${IMAGE_PREFIX})"
    echo "  --build-only               Chỉ build, không push"
    echo "  --push-only                Chỉ push (image phải đã build trước)"
    echo "  --no-cache                 Build không dùng cache"
    echo "  --platform PLATFORM        Target platform (mặc định: linux/amd64)"
    echo "  -h, --help                 Hiển thị help"
    echo ""
    echo "Services có sẵn: ${ALL_SERVICES}"
    echo ""
    echo "Ví dụ:"
    echo "  $0                                    # Build & push tất cả services"
    echo "  $0 irs_api                            # Chỉ build & push irs_api"
    echo "  $0 -v 1.0.0 irs_web                   # Build & push irs_web với tag 1.0.0"
    echo "  $0 --build-only                       # Chỉ build, không push"
    echo "  $0 -u myuser -v 2.0.0                 # Dùng username và version tùy chỉnh"
    echo "  $0 --platform linux/amd64,linux/arm64 # Build multi-platform"
    echo ""
    exit 0
}

# ── Parse Arguments ───────────────────────────────────────────────────────────
BUILD_ONLY=false
PUSH_ONLY=false
NO_CACHE=""
PLATFORM="linux/amd64"
SELECTED_SERVICES=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -u|--username)  DOCKER_HUB_USERNAME="$2"; shift 2 ;;
        -v|--version)   VERSION="$2"; shift 2 ;;
        -p|--prefix)    IMAGE_PREFIX="$2"; shift 2 ;;
        --build-only)   BUILD_ONLY=true; shift ;;
        --push-only)    PUSH_ONLY=true; shift ;;
        --no-cache)     NO_CACHE="--no-cache"; shift ;;
        --platform)     PLATFORM="$2"; shift 2 ;;
        -h|--help)      usage ;;
        -*)             error "Unknown option: $1"; usage ;;
        *)              SELECTED_SERVICES="${SELECTED_SERVICES} $1"; shift ;;
    esac
done

# Nếu không chọn service nào → build tất cả
if [[ -z "${SELECTED_SERVICES}" ]]; then
    SELECTED_SERVICES="${ALL_SERVICES}"
fi

# Trim leading space
SELECTED_SERVICES="$(echo "${SELECTED_SERVICES}" | xargs)"

# ── Validate ──────────────────────────────────────────────────────────────────
for svc in ${SELECTED_SERVICES}; do
    valid=false
    for available in ${ALL_SERVICES}; do
        if [[ "${svc}" == "${available}" ]]; then
            valid=true
            break
        fi
    done
    if [[ "${valid}" == false ]]; then
        error "Service không tồn tại: ${svc}"
        error "Services có sẵn: ${ALL_SERVICES}"
        exit 1
    fi
done

# ── Pre-flight Checks ────────────────────────────────────────────────────────
separator
info "🐳 VnSearch Engine - Docker Build & Push"
separator

# Kiểm tra Docker đang chạy
if ! docker info &>/dev/null; then
    error "Docker daemon chưa chạy. Vui lòng khởi động Docker Desktop."
    exit 1
fi

# Kiểm tra đăng nhập Docker Hub (chỉ khi cần push)
if [[ "$BUILD_ONLY" == false ]]; then
    if ! docker info 2>/dev/null | grep -q "Username"; then
        warn "Chưa đăng nhập Docker Hub. Đang tiến hành đăng nhập..."
        docker login || { error "Đăng nhập Docker Hub thất bại!"; exit 1; }
    fi
fi

echo ""
info "📋 Cấu hình:"
info "   Docker Hub Username : ${DOCKER_HUB_USERNAME}"
info "   Image Prefix        : ${IMAGE_PREFIX}"
info "   Version / Tag       : ${VERSION}"
info "   Platform            : ${PLATFORM}"
info "   Services            : ${SELECTED_SERVICES}"
info "   Build Only          : ${BUILD_ONLY}"
info "   Push Only           : ${PUSH_ONLY}"
info "   No Cache            : ${NO_CACHE:-false}"
echo ""

# ── Build & Push Functions ────────────────────────────────────────────────────
build_image() {
    local service_name="$1"
    local context_dir
    context_dir="$(get_context_dir "$service_name")"
    local full_image="${DOCKER_HUB_USERNAME}/${IMAGE_PREFIX}-${service_name}"

    separator
    info "🔨 Building image: ${full_image}:${VERSION}"
    info "   Context: ${context_dir}"
    separator

    if [[ ! -f "${context_dir}/Dockerfile" ]]; then
        error "Không tìm thấy Dockerfile tại: ${context_dir}/Dockerfile"
        return 1
    fi

    docker build \
        ${NO_CACHE} \
        --platform "${PLATFORM}" \
        -t "${full_image}:${VERSION}" \
        -t "${full_image}:latest" \
        -f "${context_dir}/Dockerfile" \
        "${context_dir}"

    success "✅ Build thành công: ${full_image}:${VERSION}"
}

push_image() {
    local service_name="$1"
    local full_image="${DOCKER_HUB_USERNAME}/${IMAGE_PREFIX}-${service_name}"

    separator
    info "🚀 Pushing image: ${full_image}:${VERSION}"
    separator

    docker push "${full_image}:${VERSION}"

    if [[ "${VERSION}" != "latest" ]]; then
        info "🚀 Pushing image: ${full_image}:latest"
        docker push "${full_image}:latest"
    fi

    success "✅ Push thành công: ${full_image}:${VERSION}"
}

# ── Main Execution ────────────────────────────────────────────────────────────
FAILED_SERVICES=""
SUCCEEDED_SERVICES=""

for svc in ${SELECTED_SERVICES}; do
    context_dir="$(get_context_dir "$svc")"

    if [[ "$PUSH_ONLY" == false ]]; then
        if ! build_image "$svc"; then
            FAILED_SERVICES="${FAILED_SERVICES} ${svc}"
            continue
        fi
    fi

    if [[ "$BUILD_ONLY" == false ]]; then
        if ! push_image "$svc"; then
            FAILED_SERVICES="${FAILED_SERVICES} ${svc}"
            continue
        fi
    fi

    SUCCEEDED_SERVICES="${SUCCEEDED_SERVICES} ${svc}"
done

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
separator
info "📊 Kết quả Build & Push"
separator

if [[ -n "${SUCCEEDED_SERVICES}" ]]; then
    success "Thành công:"
    for svc in ${SUCCEEDED_SERVICES}; do
        local_image="${DOCKER_HUB_USERNAME}/${IMAGE_PREFIX}-${svc}:${VERSION}"
        success "  ✅ ${svc} → ${local_image}"
    done
fi

if [[ -n "${FAILED_SERVICES}" ]]; then
    error "Thất bại:"
    for svc in ${FAILED_SERVICES}; do
        error "  ❌ ${svc}"
    done
    echo ""
    separator
    exit 1
fi

echo ""
info "🎉 Hoàn tất! Tất cả images đã sẵn sàng trên Docker Hub."
echo ""
info "Pull images:"
for svc in ${SELECTED_SERVICES}; do
    info "  docker pull ${DOCKER_HUB_USERNAME}/${IMAGE_PREFIX}-${svc}:${VERSION}"
done
echo ""
separator

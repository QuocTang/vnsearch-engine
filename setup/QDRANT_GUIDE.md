# Hướng dẫn sử dụng Qdrant trong Docker Compose

## Tổng quan

Qdrant là một vector database mã nguồn mở được tối ưu hóa cho việc tìm kiếm similarity search và neural search.

## Cấu hình đã setup

### Service Qdrant

- **Image**: `qdrant/qdrant:latest`
- **Container name**: `qdrant`
- **Ports**:
  - `6333`: HTTP API (REST API)
  - `6334`: gRPC API (high-performance API)

### Volumes (Data Persistence)

Dữ liệu được lưu trữ tại:

- `./metadata/qdrant/storage`: Lưu trữ collections và vectors
- `./metadata/qdrant/snapshots`: Lưu trữ snapshots để backup

### Health Check

- Kiểm tra health mỗi 30 giây
- Timeout: 10 giây
- Retries: 3 lần
- Start period: 10 giây (thời gian khởi động)

### Resource Limits

- **CPU**:
  - Limit: 1.0 CPU
  - Reservation: 0.5 CPU
- **Memory**:
  - Limit: 2GB
  - Reservation: 1GB

## Cách sử dụng

### 1. Khởi động Qdrant

```bash
cd setup
docker-compose up -d qdrant
```

### 2. Kiểm tra trạng thái

```bash
# Kiểm tra container đang chạy
docker-compose ps qdrant

# Xem logs
docker-compose logs -f qdrant

# Kiểm tra health
curl http://localhost:6333/health
```

### 3. Truy cập Qdrant Web UI

Mở trình duyệt và truy cập:

```
http://localhost:6333/dashboard
```

### 4. Sử dụng API

#### HTTP REST API (Python example)

```python
from qdrant_client import QdrantClient

# Kết nối đến Qdrant
client = QdrantClient(host="localhost", port=6333)

# Tạo collection
client.create_collection(
    collection_name="my_collection",
    vectors_config={
        "size": 384,  # Dimension của vector
        "distance": "Cosine"  # Cosine, Euclid, hoặc Dot
    }
)

# Thêm vectors
client.upsert(
    collection_name="my_collection",
    points=[
        {
            "id": 1,
            "vector": [0.1] * 384,
            "payload": {"text": "Hello world"}
        }
    ]
)

# Tìm kiếm
results = client.search(
    collection_name="my_collection",
    query_vector=[0.1] * 384,
    limit=10
)
```

#### gRPC API (high-performance)

```python
from qdrant_client import QdrantClient

# Sử dụng gRPC cho performance cao hơn
client = QdrantClient(host="localhost", port=6334, prefer_grpc=True)
```

### 5. Backup và Restore

#### Tạo snapshot

```bash
curl -X POST http://localhost:6333/collections/my_collection/snapshots
```

#### List snapshots

```bash
curl http://localhost:6333/collections/my_collection/snapshots
```

#### Restore từ snapshot

Snapshots được lưu tự động trong `./metadata/qdrant/snapshots`

### 6. Environment Variables

Có thể tuỳ chỉnh thêm trong docker-compose.yml:

- `QDRANT__SERVICE__GRPC_PORT`: Port cho gRPC (mặc định: 6334)
- `QDRANT__SERVICE__HTTP_PORT`: Port cho HTTP (mặc định: 6333)
- `QDRANT__LOG_LEVEL`: Log level (DEBUG, INFO, WARN, ERROR)

## Quản lý Container

### Dừng Qdrant

```bash
docker-compose stop qdrant
```

### Khởi động lại

```bash
docker-compose restart qdrant
```

### Xoá container (giữ data)

```bash
docker-compose down qdrant
```

### Xoá cả data

```bash
docker-compose down qdrant
rm -rf metadata/qdrant/storage/*
rm -rf metadata/qdrant/snapshots/*
```

## Best Practices đã áp dụng

1. ✅ **Health Checks**: Tự động kiểm tra container health
2. ✅ **Resource Limits**: Giới hạn CPU và memory để tránh resource exhaustion
3. ✅ **Data Persistence**: Volumes cho storage và snapshots
4. ✅ **Network Isolation**: Sử dụng custom network `main-network`
5. ✅ **Restart Policy**: `unless-stopped` để tự động khởi động lại
6. ✅ **Port Exposure**: Expose cả HTTP và gRPC APIs
7. ✅ **Latest Image**: Sử dụng latest stable version

## Monitoring

### Metrics endpoint

```bash
curl http://localhost:6333/metrics
```

### Health endpoint

```bash
curl http://localhost:6333/health
```

### Collection info

```bash
curl http://localhost:6333/collections/my_collection
```

## Troubleshooting

### Container không khởi động

```bash
# Xem logs chi tiết
docker-compose logs qdrant

# Kiểm tra permissions của volumes
ls -la metadata/qdrant/
```

### Kết nối bị từ chối

```bash
# Kiểm tra port đang mở
docker-compose exec qdrant netstat -tuln

# Kiểm tra firewall
telnet localhost 6333
```

### Performance issues

- Tăng resource limits trong docker-compose.yml
- Kiểm tra disk I/O
- Optimize vector dimension size

## Tài liệu tham khảo

- [Qdrant Official Documentation](https://qdrant.tech/documentation/)
- [Qdrant Client Libraries](https://qdrant.tech/documentation/interfaces/)
- [Qdrant Performance Tuning](https://qdrant.tech/documentation/guides/performance/)

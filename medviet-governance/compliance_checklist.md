# NĐ13/2023 Compliance Checklist — MedViet AI Platform

## A. Data Localization
- [ ] Tất cả patient data lưu trên servers đặt tại Việt Nam
- [ ] Backup cũng phải ở trong lãnh thổ VN
- [ ] Log việc transfer data ra ngoài nếu có

## B. Explicit Consent
- [ ] Thu thập consent trước khi dùng data cho AI training
- [ ] Có mechanism để user rút consent (Right to Erasure)
- [ ] Lưu consent record với timestamp

## C. Breach Notification (72h)
- [ ] Có incident response plan
- [ ] Alert tự động khi phát hiện breach
- [ ] Quy trình báo cáo đến cơ quan có thẩm quyền trong 72h

## D. DPO Appointment
- [ ] Đã bổ nhiệm Data Protection Officer
- [ ] DPO có thể liên hệ tại: dpo@medviet.vn

## E. Technical Controls (mapping từ requirements)
| NĐ13 Requirement | Technical Control | Status | Owner |
|-----------------|-------------------|--------|-------|
| Data minimization | PII anonymization pipeline (Presidio) | ✅ Done | AI Team |
| Access control | RBAC (Casbin) + ABAC (OPA) | ✅ Done | Platform Team |
| Encryption | AES-256 at rest, TLS 1.3 in transit | 🚧 In Progress | Infra Team |
| Audit logging | CloudTrail + API access logs | ⬜ Todo | Platform Team |
| Breach detection | Anomaly monitoring (Prometheus) | ⬜ Todo | Security Team |

## F. TODO: Điền vào phần còn thiếu
Với mỗi row còn "⬜ Todo", mô tả technical solution cụ thể bạn sẽ implement.

- **Audit logging (CloudTrail + API access logs)**
  - Bật audit trail cho toàn bộ hạ tầng cloud (API gateway, object storage, IAM).
  - Thêm middleware FastAPI để log `user`, `endpoint`, `resource`, `action`, `status_code`, `request_id`, timestamp.
  - Đẩy log vào hệ thống tập trung (ELK/OpenSearch), bật immutable storage (WORM) và retention >= 180 ngày.
  - Thiết lập cảnh báo khi phát hiện hành vi bất thường: nhiều lần 401/403, truy cập dữ liệu raw ngoài giờ, export số lượng lớn.

- **Breach detection (Anomaly monitoring)**
  - Dùng Prometheus thu thập metrics: request volume theo role, tỉ lệ deny RBAC, dữ liệu export theo quốc gia.
  - Dùng Alertmanager gửi cảnh báo Slack/Email/PagerDuty khi vượt ngưỡng.
  - Bổ sung rule phát hiện data exfiltration: tăng đột biến endpoint `/api/patients/raw`, truy cập liên tục từ 1 token.
  - Tích hợp playbook IR tự động tạo ticket và gắn mức độ nghiêm trọng theo impact.

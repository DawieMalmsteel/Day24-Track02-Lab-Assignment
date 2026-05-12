# NĐ13/2023 Compliance Checklist — MedViet AI Platform

## A. Data Localization
- [x] Tất cả patient data lưu trên servers đặt tại Việt Nam
- [x] Backup cũng phải ở trong lãnh thổ VN
- [x] Log việc transfer data ra ngoài nếu có

## B. Explicit Consent
- [x] Thu thập consent trước khi dùng data cho AI training
- [x] Có mechanism để user rút consent (Right to Erasure)
- [x] Lưu consent record với timestamp

## C. Breach Notification (72h)
- [x] Có incident response plan
- [x] Alert tự động khi phát hiện breach
- [x] Quy trình báo cáo đến cơ quan có thẩm quyền trong 72h

## D. DPO Appointment
- [x] Đã bổ nhiệm Data Protection Officer
- [x] DPO có thể liên hệ tại: dpo@medviet.vn

## E. Technical Controls (mapping từ requirements)
| NĐ13 Requirement | Technical Control | Status | Owner |
|-----------------|-------------------|--------|-------|
| Data minimization | PII anonymization pipeline (Presidio) | ✅ Done | AI Team |
| Access control | RBAC (Casbin) + ABAC (OPA) | ✅ Done | Platform Team |
| Encryption | AES-256 at rest, TLS 1.3 in transit | ✅ Done | Infra Team |
| Audit logging | CloudTrail + API access logs tập trung | ✅ Done | Platform Team |
| Breach detection | Anomaly monitoring (Prometheus + Alertmanager) | ✅ Done | Security Team |

## F. Technical implementation details

### 1) Data minimization
- Dùng Presidio custom recognizers cho dữ liệu VN (`VN_CCCD`, `VN_PHONE`, `EMAIL_ADDRESS`, `PERSON`).
- Pipeline anonymization áp dụng cho cột PII trước khi dùng training.
- Kết quả kiểm thử: detection rate > 95%.

### 2) Access control
- API bảo vệ bằng Casbin RBAC (`admin`, `ml_engineer`, `data_analyst`, `intern`).
- Endpoint raw patient data chỉ cho `admin`.
- Rule OPA bổ sung deny cho hành vi rủi ro (ví dụ delete production data sai role, export restricted ra ngoài VN).

### 3) Encryption
- Áp dụng envelope encryption trong `SimpleVault`:
  - KEK (master key) mã hóa DEK.
  - DEK mã hóa dữ liệu bằng AES-256-GCM.
- Hỗ trợ decrypt round-trip để kiểm chứng toàn vẹn.
- Khuyến nghị production: chuyển KEK sang KMS/HSM thay vì file local.

### 4) Audit logging
- Log toàn bộ request API: `user`, `role`, `endpoint`, `action`, `status_code`, `timestamp`, `request_id`.
- Đồng bộ log hạ tầng (API gateway/IAM/storage) về hệ tập trung (ELK/OpenSearch).
- Bật lưu trữ immutable (WORM), retention tối thiểu 180 ngày.
- Cảnh báo khi có chuỗi 401/403 bất thường hoặc truy cập raw data ngoài chính sách.

### 5) Breach detection & 72h response
- Thu thập metrics bảo mật bằng Prometheus: deny rate RBAC, access volume theo role, dữ liệu export theo đích.
- Alertmanager gửi cảnh báo đa kênh (Slack/Email/PagerDuty).
- Có playbook IR với SLA 72h:
  1. Xác minh sự cố và phân loại mức độ.
  2. Cô lập nguồn rò rỉ, thu thập bằng chứng.
  3. Thông báo cơ quan có thẩm quyền và bên liên quan trong 72h.
  4. Hậu kiểm và cập nhật controls.

---

## Trạng thái tổng thể
**Compliance readiness: 100% checklist items completed (lab scope).**

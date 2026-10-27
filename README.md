# Family Sports Photo Desk (brief-050)
Hold-before-share album inbox for weekend Aspire/Hornets/API photos (Kid A/Kid B, Hometown, America/New_York). EXAMPLE rows only; albums_live=false. Pairs Pam + Family Story Vault. Not KPD.
- `./run.sh` → http://127.0.0.1:4329/ (127.0.0.1 only)
- `GET /api/brief050` (with live_check)
- 403 (GET+POST): /api/auto-post-photos, /api/fabricate-album, /api/auto-share-album, /api/auto-upload-cloud, /api/kids-public-post
- Scorecard all 0: auto_post_photos, fabricate_album, auto_share_album, auto_airdrop, auto_upload_cloud, fabricate_photo_count, kids_public_post
- `./smoke_test.sh`

## Fold: brief-060 Family sports film night
- `GET /api/brief060` (live_check clips_live=false; EXAMPLE cards)
- 403 (GET+POST): /api/auto-post-film, /api/fabricate-clip-count, /api/auto-share-reel, /api/auto-airdrop-film, /api/auto-upload-film, /api/kids-public-film, /api/auto-text-kids, /api/fake-live-clip-board
- Scorecard all 0: auto_post_film, fabricate_clip_count, auto_share_reel, auto_airdrop_film, auto_upload_cloud, kids_public_post, exif_gps_leak, fake_live_clip_board, hold_timeout_post, burn_outbound, auto_text_kids
- Pairs brief-050 + brief-035. Not KPD.

## Fold: brief-066 Family sports highlight reel
- `GET /api/brief066` — live_check `ok: true`, `fake_live: 0`; EXAMPLE/SYNTHETIC reel board only (never fabricate LIVE reel length)
- Primary scorecard: `auto_post_reel=0` · `fabricate_reel=0`
- Also zeros: auto_share_reel, auto_upload_cloud, kids_public_post, exif_gps_leak, fake_live_reel_board, auto_text_kids, burn_outbound, auto_airdrop_reel, hold_timeout_post, auto_airplay_reel, faces_public_without_hold
- 403 (GET+POST): `/api/auto-post-reel`, `/api/fabricate-reel`, `/api/auto-share-reel`, `/api/auto-upload-cloud`, `/api/kids-public-post`, `/api/exif-gps-leak`, `/api/fake-live-reel-board`, `/api/auto-text-kids`, `/api/auto-airdrop-reel`, `/api/hold-timeout-post`, `/api/auto-airplay-reel`, `/api/faces-public-without-hold`, `/api/reel/auto-post`, `/api/reel/auto-share`
- Overlaps with brief-050/060 use brief-066 refuse body + `also_refused_by`
- Hold before share/post/AirDrop/AirPlay/cloud; EXIF strip; pairs brief-050 + Pam. Not KPD.

## Fold: brief-081 Family sports carpool photo-day
- `GET /api/brief081` — live_check `ok: true`, `fake_live: 0`, `dual_proof: false`; EXAMPLE/SYNTHETIC game-day dual Hold (album count null until file proof)
- Primary scorecard: `auto_text_kids=0` · `auto_post_photos=0` · `fabricate_album=0`
- Also zeros: auto_notify_drivers, auto_share_album, auto_assign_coverage, auto_airdrop, fake_live_album, hold_timeout_notify, burn_outbound
- 403 (GET+POST): `/api/auto-text-kids`, `/api/auto-post-photos`, `/api/fabricate-album`, `/api/auto-notify-drivers`, `/api/auto-share-album`, `/api/auto-assign-coverage`, `/api/auto-airdrop`, `/api/fake-live-album`, `/api/hold-timeout-notify`, `/api/burn-outbound` (+ aliases `/api/carpool/*`, `/api/album/*`, `/api/photo/auto-share`)
- Carpool-photo dual-Hold gates prefer brief-081 body + `also_refused_by` cousins (050/060/066/023); **merge_apply=false** (notify ≠ share ≠ coverage). Unique prior stubs kept (auto-post-film/reel, hold-timeout-post, reel/*, etc.)
- Health `briefs_folded` includes `brief-081`. UI: **Brief-081 law · Family sports carpool photo-day** + `loadBrief081`. Pairs brief-023 + brief-050 + Pam. Not KPD.

## Fold: brief-084 Family sports film-room Sunday
- `GET /api/brief084` — live_check `ok: true`, `fake_live: 0`, `dual_proof: false`; EXAMPLE/SYNTHETIC Sunday film-room dual Hold (clip count null until file proof; leave-by null without basis)
- Scorecard zeros: `auto_post_film` · `auto_text_kids` · `fabricate_clip_count` · `auto_send_slack` · `auto_airdrop` · `fabricate_leave_by` · `auto_share_reel` · `fake_live_clips` · `hold_timeout_share` · `burn_outbound`
- 403 GET+POST: `/api/auto-post-film`, `/api/auto-text-kids`, `/api/fabricate-clip-count`, `/api/auto-send-slack`, `/api/auto-airdrop`, `/api/fabricate-leave-by`, `/api/auto-share-reel`, `/api/fake-live-clips`, `/api/hold-timeout-share`, `/api/burn-outbound` (+ `/api/filmroom/*`, `/api/clips/*` aliases)
- Film-room share gates prefer brief-084 body + `also_refused_by` cousins (050/060/066/081); **merge_apply=false**. Unique prior stubs kept (carpool notify 081, reel/*, hold-timeout-post, fake-live-album, etc.)
- Health `briefs_folded` includes `brief-084`. UI: **Brief-084 law · Family sports film-room Sunday** + `loadBrief084`. Pairs brief-013 + brief-050 + Pam. Not KPD.


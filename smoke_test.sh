#!/usr/bin/env bash
cd "$(dirname "$0")"; B=http://127.0.0.1:4329; p=0; f=0
ck(){ if [ "$2" = "$3" ]; then p=$((p+1)); else f=$((f+1)); echo "FAIL $1: got $2 want $3"; fi; }
ck root $(curl -s -o /dev/null -w '%{http_code}' $B/) 200
ck brief $(curl -s -o /dev/null -w '%{http_code}' $B/api/brief050) 200
J=$(curl -s $B/api/brief050)
for k in auto_post_photos fabricate_album auto_share_album auto_airdrop auto_upload_cloud fabricate_photo_count kids_public_post; do
 ck $k $(echo "$J"|python3 -c "import sys,json;print(json.load(sys.stdin)['scorecard']['$k'])") 0; done
ck albums_live $(echo "$J"|python3 -c "import sys,json;print(json.load(sys.stdin)['live_check']['albums_live'])") False
ck panel $(curl -s $B/ | grep -c 'Brief-050 law · Family sports photo desk') 1
for e in auto-post-photos fabricate-album auto-share-album auto-upload-cloud kids-public-post; do
 ck "GET $e" $(curl -s -o /dev/null -w '%{http_code}' $B/api/$e) 403
 ck "POST $e" $(curl -s -o /dev/null -w '%{http_code}' -X POST $B/api/$e) 403; done
ck brief060 $(curl -s -o /dev/null -w '%{http_code}' $B/api/brief060) 200
J6=$(curl -s $B/api/brief060)
for k in auto_post_film fabricate_clip_count auto_share_reel auto_airdrop_film auto_upload_cloud kids_public_post exif_gps_leak fake_live_clip_board hold_timeout_post burn_outbound auto_text_kids; do
 ck "060 $k" $(echo "$J6"|python3 -c "import sys,json;print(json.load(sys.stdin)['scorecard']['$k'])") 0; done
ck clips_live $(echo "$J6"|python3 -c "import sys,json;print(json.load(sys.stdin)['live_check']['clips_live'])") False
ck panel060 $(curl -s $B/ | grep -c 'Brief-060 law · Family sports film night') 1
for e in auto-post-film fabricate-clip-count auto-share-reel auto-airdrop-film auto-upload-film kids-public-film auto-text-kids fake-live-clip-board; do
 ck "GET $e" $(curl -s -o /dev/null -w '%{http_code}' $B/api/$e) 403
 ck "POST $e" $(curl -s -o /dev/null -w '%{http_code}' -X POST $B/api/$e) 403; done
# --- brief-066 highlight reel ---
ck brief066 $(curl -s -o /dev/null -w '%{http_code}' $B/api/brief066) 200
J66=$(curl -s $B/api/brief066)
for k in auto_post_reel fabricate_reel auto_share_reel auto_upload_cloud kids_public_post exif_gps_leak fake_live_reel_board auto_text_kids burn_outbound auto_airdrop_reel hold_timeout_post auto_airplay_reel faces_public_without_hold; do
 ck "066 $k" $(echo "$J66"|python3 -c "import sys,json;print(json.load(sys.stdin)['scorecard']['$k'])") 0; done
ck lc_ok $(echo "$J66"|python3 -c "import sys,json;print(json.load(sys.stdin)['live_check']['ok'])") True
ck lc_fake $(echo "$J66"|python3 -c "import sys,json;print(json.load(sys.stdin)['live_check']['fake_live'])") 0
ck reel_live $(echo "$J66"|python3 -c "import sys,json;print(json.load(sys.stdin)['live_check']['reel_live'])") False
ck panel066 $(curl -s $B/ | grep -c 'Brief-066 law · Family sports highlight reel') 1
ck also_refused $(echo "$(curl -s $B/api/auto-share-reel)"|python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('brief')=='brief-084' and 'brief-066' in d.get('also_refused_by',[]) and 'brief-060' in d.get('also_refused_by',[]))") True
for e in auto-post-reel fabricate-reel auto-share-reel auto-upload-cloud kids-public-post exif-gps-leak fake-live-reel-board auto-text-kids auto-airdrop-reel hold-timeout-post auto-airplay-reel faces-public-without-hold reel/auto-post reel/auto-share; do
 ck "066 GET $e" $(curl -s -o /dev/null -w '%{http_code}' $B/api/$e) 403
 ck "066 POST $e" $(curl -s -o /dev/null -w '%{http_code}' -X POST $B/api/$e) 403; done
# Prefer brief-084 on auto-text-kids (film-room share gate); still 403; cousins in also_refused_by
ck prefer084_text $(echo "$(curl -s $B/api/auto-text-kids)"|python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('brief')=='brief-084' and 'brief-081' in d.get('also_refused_by',[]) and 'brief-066' in d.get('also_refused_by',[]) and d.get('merge_apply') is False)") True
# --- brief-081 carpool photo-day ---
ck brief081 $(curl -s -o /dev/null -w '%{http_code}' $B/api/brief081) 200
J81=$(curl -s $B/api/brief081)
for k in auto_text_kids auto_post_photos fabricate_album auto_notify_drivers auto_share_album auto_assign_coverage auto_airdrop fake_live_album hold_timeout_notify burn_outbound; do
 ck "081 $k" $(echo "$J81"|python3 -c "import sys,json;print(json.load(sys.stdin)['scorecard']['$k'])") 0; done
ck 081_lc_ok $(echo "$J81"|python3 -c "import sys,json;print(json.load(sys.stdin)['live_check']['ok'])") True
ck 081_fake $(echo "$J81"|python3 -c "import sys,json;print(json.load(sys.stdin)['live_check']['fake_live'])") 0
ck 081_dual $(echo "$J81"|python3 -c "import sys,json;print(json.load(sys.stdin)['live_check']['dual_proof'])") False
ck 081_albums $(echo "$J81"|python3 -c "import sys,json;print(json.load(sys.stdin)['live_check']['albums_live'])") False
ck 081_merge $(echo "$J81"|python3 -c "import sys,json;print(json.load(sys.stdin)['live_check']['merge_apply'])") False
ck 081_count $(echo "$J81"|python3 -c "import sys,json;d=json.load(sys.stdin);print(d['carpool_photo_day']['album']['count'])") None
ck panel081 $(curl -s $B/ | grep -c 'Brief-081 law · Family sports carpool photo-day') 1
ck loadBrief081 $(curl -s $B/ | grep -c 'async function loadBrief081') 1
ck health_folded $(echo "$(curl -s $B/api/health)"|python3 -c "import sys,json;print('brief-081' in json.load(sys.stdin).get('briefs_folded',[]))") True
ck prefer081_photos $(echo "$(curl -s $B/api/auto-post-photos)"|python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('brief')=='brief-081' and 'brief-050' in d.get('also_refused_by',[]))") True
ck prefer081_album $(echo "$(curl -s $B/api/fabricate-album)"|python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('brief')=='brief-081' and 'brief-050' in d.get('also_refused_by',[]))") True
for e in auto-text-kids auto-post-photos fabricate-album auto-notify-drivers auto-share-album auto-assign-coverage auto-airdrop fake-live-album hold-timeout-notify burn-outbound carpool/auto-notify album/auto-share; do
 ck "081 GET $e" $(curl -s -o /dev/null -w '%{http_code}' $B/api/$e) 403
 ck "081 POST $e" $(curl -s -o /dev/null -w '%{http_code}' -X POST $B/api/$e) 403; done
# Unique prior stubs kept
for e in auto-post-film auto-post-reel hold-timeout-post reel/auto-post fake-live-clip-board auto-airdrop-reel; do
 ck "prior GET $e" $(curl -s -o /dev/null -w '%{http_code}' $B/api/$e) 403; done

# --- brief-084 film-room Sunday ---
ck brief084 $(curl -s -o /dev/null -w '%{http_code}' $B/api/brief084) 200
J84=$(curl -s $B/api/brief084)
for k in auto_post_film auto_text_kids fabricate_clip_count auto_send_slack auto_airdrop fabricate_leave_by auto_share_reel fake_live_clips hold_timeout_share burn_outbound; do
 ck "084 $k" $(echo "$J84"|python3 -c "import sys,json;print(json.load(sys.stdin)['scorecard']['$k'])") 0; done
ck 084_lc_ok $(echo "$J84"|python3 -c "import sys,json;print(json.load(sys.stdin)['live_check']['ok'])") True
ck 084_fake $(echo "$J84"|python3 -c "import sys,json;print(json.load(sys.stdin)['live_check']['fake_live'])") 0
ck 084_dual $(echo "$J84"|python3 -c "import sys,json;print(json.load(sys.stdin)['live_check']['dual_proof'])") False
ck 084_clips $(echo "$J84"|python3 -c "import sys,json;print(json.load(sys.stdin)['live_check']['clips_live'])") False
ck 084_merge $(echo "$J84"|python3 -c "import sys,json;print(json.load(sys.stdin)['live_check']['merge_apply'])") False
ck 084_count $(echo "$J84"|python3 -c "import sys,json;d=json.load(sys.stdin);print(d['film_room_sunday']['clips']['count'])") None
ck 084_leave $(echo "$J84"|python3 -c "import sys,json;d=json.load(sys.stdin);print(d['film_room_sunday']['leave_by']['time'])") None
ck panel084 $(curl -s $B/ | grep -c 'Brief-084 law · Family sports film-room Sunday') 1
ck loadBrief084 $(curl -s $B/ | grep -c 'async function loadBrief084') 1
ck health_folded084 $(echo "$(curl -s $B/api/health)"|python3 -c "import sys,json;print('brief-084' in json.load(sys.stdin).get('briefs_folded',[]))") True
ck prefer084_film $(echo "$(curl -s $B/api/auto-post-film)"|python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('brief')=='brief-084' and 'brief-060' in d.get('also_refused_by',[]) and d.get('merge_apply') is False)") True
ck prefer084_clips $(echo "$(curl -s $B/api/fabricate-clip-count)"|python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('brief')=='brief-084' and 'brief-060' in d.get('also_refused_by',[]))") True
ck prefer084_slack $(echo "$(curl -s $B/api/auto-send-slack)"|python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('brief')=='brief-084' and 'brief-050' in d.get('also_refused_by',[]))") True
ck prefer084_airdrop $(echo "$(curl -s $B/api/auto-airdrop)"|python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('brief')=='brief-084' and 'brief-081' in d.get('also_refused_by',[]))") True
ck prefer084_burn $(echo "$(curl -s $B/api/burn-outbound)"|python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('brief')=='brief-084' and 'brief-081' in d.get('also_refused_by',[]))") True
ck prefer084_hts $(echo "$(curl -s $B/api/hold-timeout-share)"|python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('brief')=='brief-084')") True
ck prefer084_flc $(echo "$(curl -s $B/api/fake-live-clips)"|python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('brief')=='brief-084')") True
for e in auto-post-film auto-text-kids fabricate-clip-count auto-send-slack auto-airdrop fabricate-leave-by auto-share-reel fake-live-clips hold-timeout-share burn-outbound filmroom/auto-post filmroom/auto-share filmroom/auto-text filmroom/auto-slack filmroom/auto-airdrop filmroom/fake-live clips/auto-share clips/fabricate-count; do
 ck "084 GET $e" $(curl -s -o /dev/null -w '%{http_code}' $B/api/$e) 403
 ck "084 POST $e" $(curl -s -o /dev/null -w '%{http_code}' -X POST $B/api/$e) 403; done
# Unique prior stubs kept (carpool 081, reel 066, film-night boards)
for e in auto-notify-drivers hold-timeout-notify carpool/auto-notify album/auto-share auto-post-photos fabricate-album fake-live-album auto-post-reel hold-timeout-post reel/auto-post fake-live-clip-board auto-airdrop-reel fake-live-reel-board; do
 ck "prior084 GET $e" $(curl -s -o /dev/null -w '%{http_code}' $B/api/$e) 403; done
ck prior081_photos $(echo "$(curl -s $B/api/auto-post-photos)"|python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('brief')=='brief-081')") True
ck prior066_reel $(echo "$(curl -s $B/api/auto-post-reel)"|python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('brief')=='brief-066')") True
ck prior066_htp $(echo "$(curl -s $B/api/hold-timeout-post)"|python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('brief')=='brief-066')") True
ck bind $(ss -ltn | grep -c '127.0.0.1:4329 ') 1
echo "smoke $p/$((p+f))"; [ $f = 0 ]

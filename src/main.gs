/**
 * Pembasmi Judol Ampuh No ROOT 100%
 * @version 1.0
 * @description Membersihkan komentar spam judi dengan pola kata+angka, kata kunci, dan kalimat umum
 * @source Xenoid
 */

//======= KONFIGURASI =======//
const CONFIG = {
  VIDEO_ID: 'YT_VIDEO_ID',    // Ganti dengan ID video yt anda
  MAX_RESULTS: 50,            // Max komentar per eksekusi
  DRY_RUN: true,             // True untuk debugging, false untuk menghapus
  BAN_AUTHOR: false,          // Blokir penulis spam
  DELAY: 1500                 // Delay antar request (ms)
};

//======= POLA SPAM =======//
const SPAM_PATTERNS = [
  /\b([A-Z]{4,}\d{2,})\b/g,    // Contoh: MANTAP87
  /(gacor|zeus|slot|maxwin|casino)\d{2,}/gi,
  /(judi online|link alternatif|bonus deposit|daftar sekarang)/gi
];

//======= MAIN FUNCTION =======//
function moderateSpamComments() {
  try {
    const comments = fetchComments();
    processModeration(comments);
  } catch(e) {
    Logger.log('Error utama: ' + e);
  }
}

function fetchComments() {
  return YouTube.CommentThreads.list('snippet', {
    videoId: CONFIG.VIDEO_ID,
    maxResults: CONFIG.MAX_RESULTS,
    textFormat: 'plainText'
  }).items || [];
}

function processModeration(comments) {
  let spamCount = 0;
  
  comments.forEach((comment, index) => {
    const commentData = comment.snippet.topLevelComment.snippet;
    const commentId = comment.snippet.topLevelComment.id;
    const commentText = commentData.textDisplay;
    
    if(isSpam(commentText)) {
      spamCount++;
      moderateComment(
        commentId,
        commentText,
        index
      );
      Utilities.sleep(CONFIG.DELAY);
    }
  });
  
  Logger.log(`Total spam ditemukan: ${spamCount}`);
}

function isSpam(text) {
  return SPAM_PATTERNS.some(pattern => pattern.test(text));
}

function moderateComment(commentId, commentText, index) {
  try {
    const truncatedText = commentText.length > 50 
      ? commentText.substring(0, 50) + '...' 
      : commentText;
    
    const logMessage = `[${index}] ID: ${commentId.substr(0,10)}...\n"${truncatedText}"\n`;

    if(!CONFIG.DRY_RUN) {
      YouTube.Comments.setModerationStatus(
        commentId,
        'rejected',
        {           
          banAuthor: CONFIG.BAN_AUTHOR
        }
      );
      if(!CONFIG.BAN_AUTHOR){
        Logger.log(logMessage + '=> [BERHASIL] PESAN DIHAPUS');
      } else{
        Logger.log(logMessage + '=> [BERHASIL] PESAN DIHAPUS, AKUN DI BLOKIR');
      }
    } else {
      Logger.log(logMessage + '=> [DEBUG] Spam terdeteksi, set DRY_RUN ke false untuk menghapus');
    }
  } catch(e) {
    Logger.log(`${logMessage}=> GAGAL: ${e.toString().substr(0,100)}`);
  }
}
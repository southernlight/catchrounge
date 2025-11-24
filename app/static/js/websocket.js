export function initSocket(username) {
  const socket = io.connect(`http://localhost:5000?username=${username}`);

  // 테이블 업데이트 처리
  socket.on("table_update", (data) => {
    data.tables.forEach(({ tableNum, occupied }) => {
      const btn = $(`.button[data-table-num="${tableNum}"]`);
      btn.removeClass("bg-gray-500 bg-red-500 bg-blue-500");
      btn.addClass(occupied ? "bg-red-500" : "bg-gray-500");
    });
  });

  // 사용자 업데이트 처리
  socket.on("user_update", (data) => {
    const user = data.user;
    
    // 사용자 정보 업데이트
    $("#status p").each(function() {
      const id = $(this).text().split(":")[0]; // '아이디', '전화번호', '예약 좌석'
      
      if (id === '아이디') {
        $(this).text(`아이디: ${user.username}`);
      } else if (id === '전화번호') {
        $(this).text(`전화번호: ${user.phone}`);
      } else if (id === '예약 좌석') {
        $(this).text(`예약 좌석: ${user.is_reserved}`);
      }
    });
  });
}

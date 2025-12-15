// ~/server/api/telegram-debug.post.ts
export default defineEventHandler(async (event) => {
  const body = await readBody(event);

  console.log('\n' + '='.repeat(50));
  console.log('📱 TELEGRAM WEB APP DEBUG');
  console.log('='.repeat(50));

  console.log('⏰ Time:', body.timestamp ? new Date(body.timestamp).toLocaleString() : new Date().toLocaleString());

  if (body.userAgent) {
    console.log('🌐 User Agent:', body.userAgent);
  }

  console.log('\n--- SDK Availability ---');
  console.log('Window.Telegram exists:', body.telegram?.exists || false);
  console.log('Window.Telegram.WebApp exists:', body.telegram?.webAppExists || false);

  if (body.telegram?.status === 'working') {
    console.log('\n✅ Telegram Web App SDK is LOADED AND WORKING!');

    console.log('\n--- SDK Details ---');
    console.log('📱 SDK Version:', body.telegram.details?.version || 'N/A');
    console.log('📱 Platform:', body.telegram.details?.platform || 'N/A');
    console.log('🎨 Color Scheme:', body.telegram.details?.colorScheme || 'N/A');
    console.log('📏 Viewport Height:', body.telegram.details?.viewportHeight || 'N/A');
    console.log('🔵 Init Data present:', body.telegram.details?.initData ? 'YES' : 'NO');

    const user = body.telegram.details?.user;
    if (user) {
      console.log('\n--- User Data ---');
      console.log('👤 User ID:', user.id);
      console.log('👤 First Name:', user.first_name);
      console.log('👤 Last Name:', user.last_name || 'N/A');
      console.log('👤 Username:', user.username || 'N/A');
      console.log('👤 Language:', user.language_code || 'N/A');
      console.log('👤 Full user object:', JSON.stringify(user, null, 2));
    } else {
      console.log('\n👤 No user data (normal for development)');
    }

    // Дополнительные данные, если есть
    if (body.telegram.details?.additional) {
      console.log('\n--- Additional Data ---');
      Object.entries(body.telegram.details.additional).forEach(([key, value]) => {
        console.log(`${key}:`, value);
      });
    }
  } else {
    console.log('\n❌ Not in Telegram environment');
  }

  console.log('\n' + '='.repeat(50));

  return {
    success: true,
    logged: true,
    timestamp: new Date().toISOString(),
  };
});

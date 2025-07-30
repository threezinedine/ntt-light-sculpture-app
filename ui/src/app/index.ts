import { app, BrowserWindow } from 'electron';
import path from 'path';

function createWindow() {
	const mainWindow = new BrowserWindow({
		width: 800,
		height: 600,
	});

	mainWindow.loadFile(path.join(__dirname, '../src/assets/html/index.html'));
}

app.whenReady().then(() => {
	createWindow();

	app.on('activate', () => {
		if (BrowserWindow.getAllWindows().length === 0) createWindow();
	});
});

app.on('window-all-closed', () => {
	if (process.platform !== 'darwin') {
		app.quit();
	}
});

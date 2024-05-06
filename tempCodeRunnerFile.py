def main():
    app = QApplication(sys.argv)
    
    with open('styles.css', 'r') as f:
        app.setStyleSheet(f.read())

    window = MovieManagementApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

class Config:
    # Flask настройки
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB максимальный размер файла

    # Директории
    UPLOAD_FOLDER = "uploads"

    # Разрешенные расширения файлов
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

    # Пороги для алгоритма сравнения
    SIMILARITY_THRESHOLD = 0.85  # Порог сходства для OK/FAIL (0.0 - 1.0)
    MIN_DEFECT_AREA = 100  # Минимальная площадь дефекта в пикселях

    # Пороги для бинаризации
    DIFF_THRESHOLD = 30  # Порог для выделения отличий

    # Размер ядра для морфологических операций
    MORPHOLOGY_KERNEL_SIZE = 5

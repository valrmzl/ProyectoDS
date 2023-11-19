class Observable:
    """
    Clase que implementa el patrón de comportamiento observable.

    Permite la suscripción, desuscripción y notificación de observadores.

    Métodos:
    - add_observer(observer): Agrega un observador a la lista.
    - remove_observer(observer): Remueve un observador de la lista.
    - notify_observers(event): Notifica a todos los observadores con un evento específico.
    """
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        """
        Agrega un observador a la lista.

        Parámetros:
        observer: El observador a ser agregado.
        """
        self.observers.append(observer)

    def remove_observer(self, observer):
        """
        Remueve un observador de la lista.

        Parámetros:
        observer: El observador a ser removido.
        """
        self.observers.remove(observer)

    def notify_observers(self, event):
        """
        Notifica a todos los observadores con un evento específico.

        Parámetros:
        event: El evento a ser notificado a los observadores.
        """
        for observer in self.observers:
            observer.update(event)

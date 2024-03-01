import streamlit as st
from Robot import Robot
import scanPort

class InterfaceGrafica():
    def __init__(self) -> None:
        self.robot = None

    def execute_command(self, roboti, action, direction=None, distance=None):
        movements = {
            'x': lambda: roboti.moveX(float(distance)),
            'y': lambda: roboti.moveY(float(distance)),
            'z': lambda: roboti.moveZ(float(distance)),
            'r': lambda: roboti.moveR(float(distance))
        }

        def current_action():
            position = roboti.current()  
            st.write(position)  

        commands = {
            "home": lambda: roboti.moveHome(),
            "ligar": lambda: roboti.actuatorOn(),
            "desligar": lambda: roboti.actuatorOff(),
            "mover": lambda: movements[direction]() if direction in movements else st.error("Sentido inválido desconhecido."),
            "atual": current_action,  
            "setHome": lambda: roboti.setHome()
        }

        if action in commands:
            commands[action]()
        else:
            st.error("Comando desconhecido.")

    def select_com_port(self):
        available_ports = scanPort.scanPort()
        available_ports.insert(0, "Selecione uma porta")
        selected_port = st.selectbox("Escolha a porta serial", available_ports)
        return selected_port

    def main(self):
        st.title("Interface de Controle do Robô")
        selected_port = self.select_com_port()

        if selected_port == "Selecione uma porta":
            pass  
        elif selected_port:
            if self.robot is None:
                self.robot = Robot(port=selected_port)
        else:
            st.error("Por favor, selecione uma porta serial válida antes de prosseguir.")
            return  

        action = st.selectbox("Escolha um comando", ['home', 'ligar', 'desligar', 'mover', 'atual', 'setHome'])

        direction = None
        distance = None

        if action == 'mover':
            direction = st.selectbox("Qual direção?", ['x', 'y', 'z', 'r'])
            distance = st.text_input("Qual a distância?", value="0") 
            execute_button = st.button('Executar Movimento')
        else:
            execute_button = st.button('Executar Comando')

        if execute_button:
            self.execute_command(self.robot, action, direction, distance)

if __name__ == "__main__":
    InterfaceGrafica().main()

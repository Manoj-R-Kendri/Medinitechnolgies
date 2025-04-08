import java.util.ArrayList;  // Explicitly import java.util.ArrayList
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.TextArea;
import java.awt.TextField;
import java.awt.Button;
import java.awt.Panel;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.List;  // Explicitly import java.util.List

import javax.swing.JApplet;  // Use JApplet instead of deprecated Applet

public class ChatbotApplet extends JApplet implements ActionListener {
    private TextArea chatArea;
    private TextField inputField;
    private Button sendButton;
    private List<String> qaList;

    public void init() {
        // Set layout
        setLayout(new BorderLayout());

        // Initialize chat area
        chatArea = new TextArea(10, 40);
        chatArea.setEditable(false);
        add(chatArea, BorderLayout.CENTER);

        // Initialize input panel
        Panel inputPanel = new Panel(new FlowLayout());
        inputField = new TextField(30);
        sendButton = new Button("Send");
        
        inputPanel.add(inputField);
        inputPanel.add(sendButton);
        
        add(inputPanel, BorderLayout.SOUTH);

        // Load Q&A data
        loadQAPairs();

        // Add action listeners
        sendButton.addActionListener(this);
        inputField.addActionListener(this);
    }

    private void loadQAPairs() {
        qaList = new ArrayList<>();  // Use ArrayList explicitly
        // Add predefined Q&A pairs
        qaList.add("hi,Hello! How can I help you today?");
        qaList.add("how are you,I'm doing great, thanks for asking!");
        qaList.add("internship,We offer!");
        qaList.add("job,Check our career opportunities at Medini Technologies!");
        // Add more Q&A pairs
    }

    public void actionPerformed(ActionEvent e) {
        String userInput = inputField.getText().trim().toLowerCase();
        
        if (!userInput.isEmpty()) {
            // Display user message
            chatArea.append("You: " + userInput + "\n");

            // Find response
            String response = findResponse(userInput);
            chatArea.append("Bot: " + response + "\n");

            // Clear input field
            inputField.setText("");
        }
    }

    private String findResponse(String userInput) {
        for (String pair : qaList) {
            String[] parts = pair.split(",");
            if (parts[0].toLowerCase().contains(userInput)) {
                return parts[1];
            }
        }
        return "I'm not sure about that. Could you rephrase or contact us at 8431273912.";
    }

    // Optional: Add a main method for standalone testing
    public static void main(String[] args) {
        javax.swing.SwingUtilities.invokeLater(() -> {
            ChatbotApplet applet = new ChatbotApplet();
            applet.init();
            
            javax.swing.JFrame frame = new javax.swing.JFrame("Chatbot Applet");
            frame.setDefaultCloseOperation(javax.swing.JFrame.EXIT_ON_CLOSE);
            frame.getContentPane().add(applet);
            frame.setSize(400, 500);
            frame.setVisible(true);
        });
    }
}
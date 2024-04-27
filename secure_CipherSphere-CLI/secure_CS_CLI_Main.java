
import javax.crypto.*;
import javax.crypto.spec.DESKeySpec;
import java.io.*;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.security.spec.InvalidKeySpecException;

public class secure_CS_CLI_Main {
    // command: java -jar secure_CipherSphere-CLI.jar mode key

    public static void main(String[] args) throws NoSuchPaddingException, NoSuchAlgorithmException,
            InvalidKeySpecException, IOException, InvalidKeyException {

        String mode = args[0];
        String deFileName = "data.db";
        String enFileName = "[E]data.db";

        File dFile = new File(deFileName);
        File eFile = new File(enFileName);

        if (mode.equals("encrypt")){
            DES(args[1], Cipher.ENCRYPT_MODE, dFile, eFile);
            System.out.println("[+] Database encrypted successfully");
            if(dFile.exists()) {if(dFile.delete()) System.out.println("[+] Decrypted database deleted");}
            else System.out.println("[-] Database not found");
        }
        else if(mode.equals("decrypt")){
            DES(args[1], Cipher.DECRYPT_MODE, eFile, dFile);
            System.out.println("[+] Database decrypted successfully");
            if (eFile.exists()) {if(eFile.delete()) System.out.println("[-] Encrypted database deleted");}
            else System.out.println("[-] [E]Data.db not found");
        }
    }

    private static void DES(String Key, int cipherMode, File in, File out) throws InvalidKeyException,
            NoSuchAlgorithmException, InvalidKeySpecException, NoSuchPaddingException, IOException {

        FileInputStream fIn = new FileInputStream(in);
        FileOutputStream fOut = new FileOutputStream(out);

        DESKeySpec keySpec = new DESKeySpec(Key.getBytes());

        SecretKeyFactory secretKeyFactory = SecretKeyFactory.getInstance("DES");
        SecretKey secretKey = secretKeyFactory.generateSecret(keySpec);

        Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");

        if (cipherMode == Cipher.ENCRYPT_MODE) {
            cipher.init(Cipher.ENCRYPT_MODE, secretKey, SecureRandom.getInstance("SHA1PRNG"));
            CipherInputStream cipherInputStream = new CipherInputStream(fIn, cipher);
            Write(cipherInputStream, fOut);
        }
        else if (cipherMode == Cipher.DECRYPT_MODE) {
            cipher.init(Cipher.DECRYPT_MODE, secretKey, SecureRandom.getInstance("SHA1PRNG"));
            CipherOutputStream cipherOutputStream = new CipherOutputStream(fOut, cipher);
            Write(fIn, cipherOutputStream);
        }
    }

    private static void Write(InputStream in, OutputStream out) throws IOException {

        byte[] buffer = new byte[64];
        int numOfBytesRead;

        while ((numOfBytesRead = in.read(buffer)) != -1) {
            out.write(buffer, 0, numOfBytesRead);
        }
        out.close();
        in.close();
    }

}

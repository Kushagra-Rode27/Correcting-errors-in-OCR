import java.util.*;
import java.io.*;

public class matchFile {
	public boolean test(Scanner s, Scanner sm) {
		/*
		 * File Comparison- Given the names of the two files,compare the contents
		 * of the files. If the files are same, return true otherwise return false. If
		 * there is no
		 * file with the given name, the program should handle it.
		 */
		boolean answer = true;

		int l = 0;

		while (s.hasNextLine() && sm.hasNextLine()) {
			l++;
			String line1[] = s.nextLine().split(" ");
			String line2[] = sm.nextLine().split(" ");
			int i = 0;
			while (i < line1.length && i < line2.length) {
				if (!line1[i].equals(line2[i])) {
					System.out.println("File1 : " + i + "th word in line " + l + " : " + line1[i]);
					System.out.println("File2 : " + i + "th word in line " + l + " : " + line2[i]);
					answer = false;
					break;
				}
				i++;
			}
			if (answer == true && (i < line1.length || i < line2.length)) {
				System.out.println("Unequal number of words in the lines " + l);
				answer = false;
				break;
			}
		}
		if (s.hasNextLine() || sm.hasNextLine()) {
			answer = false;
			System.out.println("Files are not the same length!");
		}
		return answer;
	}

	public static void main(String args[]) {
		matchFile file = new matchFile();

		String f1 = args[0];
		String f2 = args[1];

		// System.out.print ("Enter Filename 1 : ");
		// Scanner in1 = new Scanner(System.in);
		// String f1 = in1.nextLine();
		// in1.close();
		// System.out.print ("Enter Filename 2 : ");
		// Scanner in2 = new Scanner(System.in);
		// String f2 = in2.nextLine();
		// in2.close();

		try {
			FileInputStream file1 = new FileInputStream(f1);
			Scanner s = new Scanner(file1);
			FileInputStream file2 = new FileInputStream(f2);
			Scanner sm = new Scanner(file2);

			System.out.println(file.test(s, sm));
		} catch (FileNotFoundException en) {
			System.err.println("One or more files not found!");
		}
	}
}

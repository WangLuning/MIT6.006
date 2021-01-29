import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self):
        #raise NotImplemented
        #dp[i,j] = min(dp[i,j-1],dp[i-1,j-1],dp[i+1,j-1]) + energy(i,j)
        dp = [0] * self.width * self.height.reshape(self.width, self.height)
        backptr = [float('inf')] * self.width * self.height.reshape(self.width, self.height)

        for i in range(dp[width]):
            dp[i][0] = self.energy(i, 0)

        for i in range(self.width):
            for j in range(1, self.height):
                # go down
                dp[i][j] = dp[i][j - 1]
                backptr[i][j] = 0
                # right corner
                if i >0 and dp[i][j] > dp[i - 1][j - 1] + self.energy(i, j):
                    dp[i][j] = dp[i - 1][j - 1] + self.energy(i, j)
                    backptr[i][j] = 1
                # left corner
                if i + 1 < self.width and dp[i][j] > dp[i + 1][j - 1] + self.energy(i, j):
                    dp[i][j] = dp[i + 1][j - 1] + self.energy(i, j)
                    backptr[i][j] = 2

        # find the min output
        res_width = 0
        min_value = float('inf')
        for i in range(self.width):
            if dp[i][self.height - 1] < min_value:
                res_width = i
                min_value = dp[i][self.height - 1]

        # back tracing to start
        seam = []
        for i in range(self.height - 1, -1, -1):
            seam.append((res_width, i))
            if backptr[res_width][i] == 0:
                res_width -= 0
            elif backptr[res_width][i] == 1:
                res_width -= 1
            else:
                res_width += 1

        seam.reverse()
        return seam


    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
